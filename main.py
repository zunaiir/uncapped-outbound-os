import os
import json
from datetime import datetime, timezone
from urllib import request as urlrequest
from urllib.error import HTTPError

from flask import Flask, Response, jsonify, request

app = Flask(__name__)

APP_VERSION = "uncapped-outbound-engine-v3-live"
MAX_RESULTS = 6

PLAYBOOKS = {
    "inventory": {
        "name": "Inventory Expansion",
        "goal": "Fund inventory expansion",
        "signal_terms": [
            "new product launch",
            "new collection",
            "new category",
            "retail expansion",
            "wholesale expansion",
            "store expansion",
            "inventory",
            "distribution expansion",
        ],
        "thesis": "The company may need to fund more inventory before the resulting customer revenue is realized.",
    },
    "marketplace": {
        "name": "Marketplace Expansion",
        "goal": "Target marketplace growth",
        "signal_terms": [
            "Amazon launch",
            "Amazon expansion",
            "Walmart marketplace",
            "marketplace expansion",
            "new marketplace",
            "retail marketplace",
            "seller expansion",
        ],
        "thesis": "Marketplace expansion can require additional inventory while introducing settlement and cash-conversion timing.",
    },
    "paid": {
        "name": "Paid Growth",
        "goal": "Target paid growth",
        "signal_terms": [
            "paid acquisition",
            "performance marketing",
            "growth marketing",
            "customer acquisition",
            "marketing expansion",
            "DTC growth",
            "ecommerce growth",
        ],
        "thesis": "Growth spend may be paid before the resulting customer revenue is fully realized.",
    },
    "seasonal": {
        "name": "Seasonality",
        "goal": "Target seasonal demand",
        "signal_terms": [
            "holiday collection",
            "seasonal launch",
            "peak season",
            "holiday inventory",
            "Black Friday",
            "summer collection",
            "seasonal demand",
        ],
        "thesis": "Seasonal demand can require concentrated inventory investment well before the selling window.",
    },
}

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Uncapped Outbound Engine</title>
<meta name="description" content="A signal-led outbound engine concept built for Uncapped." />
<style>
:root{
  --bg:#f5f2ea;--surface:#fffdf7;--ink:#171916;--muted:#70766e;--line:#dcd7cb;
  --green:#66e39b;--green-dark:#143d2b;--violet:#6558ff;--violet-soft:#efedff;
  --orange:#f39b52;--orange-soft:#fff0e1;--red:#d95362;--red-soft:#fff0f2;
  --shadow:0 18px 60px rgba(27,31,26,.08);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
body{min-height:100vh;background:radial-gradient(circle at 87% 0%,rgba(101,88,255,.10),transparent 28%),radial-gradient(circle at 0% 26%,rgba(102,227,155,.09),transparent 22%),var(--bg)}
button,input,select{font:inherit}button{cursor:pointer}.shell{max-width:1260px;margin:0 auto;padding:24px 26px 54px}
.topbar{display:flex;justify-content:space-between;align-items:center;padding-bottom:22px;border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:11px}.mark{width:39px;height:39px;border-radius:50%;background:var(--ink);color:var(--green);display:grid;place-items:center;font-size:19px;font-weight:900}
.brand-copy small{display:block;font-size:9px;letter-spacing:.15em;font-weight:900;color:var(--muted)}.brand-copy strong{display:block;margin-top:2px;font-size:17px;letter-spacing:-.02em}
.prototype{display:flex;align-items:center;gap:7px;font-size:9px;color:var(--muted);border:1px solid var(--line);background:rgba(255,253,247,.75);padding:7px 10px;border-radius:999px;font-weight:750}
.prototype i{width:7px;height:7px;border-radius:50%;background:var(--green)}
.hero{padding:60px 0 38px;max-width:980px}.kicker{font-size:9px;letter-spacing:.17em;text-transform:uppercase;font-weight:900;color:var(--violet)}
.hero h1{font-size:62px;line-height:.99;letter-spacing:-.055em;max-width:950px;margin:14px 0 18px}.hero h1 em{font-style:normal;position:relative;white-space:nowrap;color:var(--green-dark)}
.hero h1 em:after{content:"";position:absolute;left:-2px;right:-2px;bottom:2px;height:10px;background:var(--green);z-index:-1;border-radius:999px;transform:rotate(-.8deg)}
.hero p{font-size:16px;line-height:1.65;color:var(--muted);max-width:760px;margin:0}.hero-strip{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:22px}
.hero-strip span{font-size:9px;font-weight:850;padding:7px 9px;border-radius:999px;border:1px solid var(--line);background:rgba(255,253,247,.7);color:#596057}.hero-strip b{color:var(--ink)}
.flow-label{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-bottom:10px}.flow-label div{display:flex;align-items:center;gap:8px;font-size:9px;font-weight:850;color:#71776f}
.flow-label span{width:23px;height:23px;border-radius:50%;display:grid;place-items:center;background:var(--ink);color:white;font-size:8px}.flow-label div:nth-child(2) span{background:var(--violet)}.flow-label div:nth-child(3) span{background:var(--green-dark);color:var(--green)}
.engine{display:grid;grid-template-columns:300px minmax(0,1fr);gap:14px;align-items:start}.builder{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:17px;box-shadow:var(--shadow);position:sticky;top:16px}
.builder h2{font-size:15px;margin:0 0 5px;letter-spacing:-.025em}.builder>p{font-size:9.5px;color:var(--muted);line-height:1.5;margin:0 0 17px}.field{margin-bottom:12px}
.field label{display:block;font-size:8px;letter-spacing:.12em;text-transform:uppercase;font-weight:900;color:#7c827a;margin-bottom:6px}.field select,.field input{width:100%;border:1px solid var(--line);border-radius:10px;background:#faf8f2;color:var(--ink);padding:10px 11px;font-size:10.5px;outline:none}
.field select:focus,.field input:focus{border-color:#a9a2ff;box-shadow:0 0 0 3px rgba(101,88,255,.08)}.generate{width:100%;border:0;border-radius:11px;background:var(--ink);color:white;padding:12px;font-size:10.5px;font-weight:900;margin-top:2px}
.generate:hover{background:#282b27}.generate:disabled{opacity:.55;cursor:wait}.builder-foot{margin-top:13px;padding-top:11px;border-top:1px solid var(--line);font-size:8.7px;line-height:1.5;color:#8a9088}
.warning{display:none;margin-top:11px;padding:10px;border:1px solid #efc7cd;background:var(--red-soft);color:#983943;border-radius:10px;font-size:9px;line-height:1.45}
.output{display:flex;flex-direction:column;gap:14px}.section{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:18px;box-shadow:0 10px 36px rgba(27,31,26,.045)}
.section-head{display:flex;justify-content:space-between;align-items:flex-start;gap:15px;margin-bottom:14px}.section-head small{display:block;font-size:8px;letter-spacing:.13em;text-transform:uppercase;font-weight:900;color:#828880;margin-bottom:5px}
.section-head h3{font-size:17px;letter-spacing:-.025em;margin:0}.section-head p{max-width:420px;font-size:9px;line-height:1.45;color:var(--muted);margin:0;text-align:right}
.logic-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}.logic{border:1px solid var(--line);border-radius:12px;padding:10px;background:#faf8f2}.logic span{display:block;font-size:7.5px;letter-spacing:.09em;text-transform:uppercase;color:#8a8f88;font-weight:900;margin-bottom:5px}.logic strong{font-size:10px;line-height:1.4}
.accounts{display:flex;flex-direction:column;gap:8px}.account{border:1px solid #e3ded2;background:#fcfaf5;border-radius:15px;display:grid;grid-template-columns:54px minmax(0,1fr) 255px;gap:12px;padding:11px;align-items:center}
.score{width:44px;height:44px;border-radius:50%;background:var(--green-dark);color:var(--green);display:grid;place-items:center;font-size:13px;font-weight:900}.account-name strong{display:block;font-size:11px;margin-bottom:3px}
.account-name span{font-size:8.8px;color:var(--muted)}.account-name .tags{display:flex;gap:4px;flex-wrap:wrap;margin-top:6px}.tag{padding:4px 6px;border-radius:999px;font-size:7.5px;font-weight:850;background:var(--violet-soft);color:#4e46a6}
.reason{border-left:1px solid var(--line);padding-left:12px}.reason small{display:block;font-size:7.5px;color:#8a8f88;font-weight:900;letter-spacing:.08em;margin-bottom:4px}.reason p{font-size:9px;line-height:1.42;margin:0;color:#565c55}
.evidence{display:inline-block;margin-top:6px;font-size:7.5px;color:var(--violet);font-weight:850;text-decoration:none;max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.evidence:hover{text-decoration:underline}
.empty{border:1px dashed var(--line);border-radius:14px;padding:35px;text-align:center;color:var(--muted);font-size:10px}
.play-layout{display:grid;grid-template-columns:.8fr 1.2fr;gap:12px}.play-summary{background:var(--ink);color:white;border-radius:16px;padding:15px}.play-summary small{font-size:8px;color:var(--green);letter-spacing:.12em;font-weight:900}
.play-summary h4{font-size:18px;letter-spacing:-.03em;margin:8px 0 7px}.play-summary p{font-size:9.5px;line-height:1.5;color:#abb4ab;margin:0}.hypothesis{margin-top:12px;border-top:1px solid #303630;padding-top:11px}.hypothesis b{display:block;font-size:8px;color:#879188;margin-bottom:5px}.hypothesis span{font-size:9.5px;line-height:1.45;color:#d8dfd9}
.message{border:1px solid var(--line);border-radius:16px;padding:14px;background:#fcfaf5}.message-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px}.message-top strong{font-size:10px}.copy{border:0;background:var(--violet-soft);color:#4e46a6;border-radius:8px;padding:6px 8px;font-size:8px;font-weight:900}
.subject{font-size:8.5px;font-weight:900;color:#575c56;margin-bottom:10px}.email{white-space:pre-wrap;font-size:10.5px;line-height:1.62;color:#40453f;margin:0}
.sequence{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:11px}.touch{border:1px solid var(--line);background:#faf8f2;border-radius:11px;padding:9px;position:relative}.touch:not(:last-child):after{content:"→";position:absolute;right:-8px;top:50%;transform:translateY(-50%);color:#8a9088}.touch span{font-size:7px;color:#8a8f88;display:block;margin-bottom:4px}.touch strong{font-size:9px}
.support{display:grid;grid-template-columns:1fr 1fr;gap:10px}.support-card{border:1px solid var(--line);border-radius:14px;padding:12px;background:#faf8f2}.support-card small{display:block;font-size:7.5px;letter-spacing:.1em;font-weight:900;text-transform:uppercase;color:#838981;margin-bottom:6px}
.support-card strong{display:block;font-size:12px;margin-bottom:5px}.support-card p{font-size:8.7px;line-height:1.45;color:var(--muted);margin:0}.capacity{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.capacity span{font-size:7.5px;padding:5px 6px;border-radius:999px;background:white;border:1px solid var(--line)}
.pipeline{display:flex;align-items:center;gap:5px;margin-top:9px;flex-wrap:wrap}.pipeline b{font-size:8px}.pipeline i{font-style:normal;color:#999f98;font-size:8px}
footer{display:flex;justify-content:space-between;gap:20px;margin-top:34px;border-top:1px solid var(--line);padding-top:17px;color:#8a9088;font-size:8.5px}
@media(max-width:900px){.hero h1{font-size:49px}.engine{grid-template-columns:1fr}.builder{position:static}.account{grid-template-columns:54px 1fr}.reason{grid-column:2;border-left:0;padding-left:0}.play-layout{grid-template-columns:1fr}}
@media(max-width:620px){.shell{padding:18px 12px 40px}.hero{padding-top:42px}.hero h1{font-size:39px}.flow-label{grid-template-columns:1fr}.logic-grid{grid-template-columns:1fr 1fr}.support{grid-template-columns:1fr}.sequence{grid-template-columns:1fr 1fr}.touch:not(:last-child):after{display:none}.section-head{display:block}.section-head p{text-align:left;margin-top:7px}}
</style>
</head>
<body>
<div class="shell">
<header class="topbar">
  <div class="brand"><div class="mark">u</div><div class="brand-copy"><small>BUILT FOR UNCAPPED</small><strong>Outbound Engine</strong></div></div>
  <div class="prototype"><i></i> live signal research</div>
</header>

<section class="hero">
  <div class="kicker">Signal-led ecommerce outbound</div>
  <h1>Find companies with a reason to need capital <em>right now.</em></h1>
  <p>Define the campaign. Surface high-fit ecommerce accounts with a timely financing hypothesis. Route each one into the right outbound play — without turning the workflow into another pile of disconnected tools.</p>
  <div class="hero-strip"><span><b>1.</b> Define the segment</span><span><b>2.</b> Find + score accounts</span><span><b>3.</b> Build the outbound play</span></div>
</section>

<div class="flow-label"><div><span>01</span> DEFINE THE CAMPAIGN</div><div><span>02</span> FIND THE OPPORTUNITY</div><div><span>03</span> BUILD THE OUTBOUND</div></div>

<main class="engine">
  <aside class="builder">
    <h2>Build a campaign</h2>
    <p>Choose the motion. Tavily finds live signals; OpenAI turns them into targeting, account hypotheses and an outbound play.</p>
    <div class="field"><label>Goal</label><select id="goal"><option value="inventory">Fund inventory expansion</option><option value="marketplace">Target marketplace growth</option><option value="paid">Target paid growth</option><option value="seasonal">Target seasonal demand</option></select></div>
    <div class="field"><label>Market</label><select id="market"><option>United States</option><option>United Kingdom</option><option>North America</option><option>Europe</option></select></div>
    <div class="field"><label>Company type</label><select id="type"><option>DTC ecommerce brands</option><option>Marketplace sellers</option><option>Omnichannel brands</option><option>Subscription ecommerce</option></select></div>
    <div class="field"><label>Weekly volume</label><input type="number" id="volume" value="500" min="100" max="5000" /></div>
    <button class="generate" id="generate">Find live opportunities</button>
    <div class="builder-foot">Live research is evidence-backed. The tool does not claim a company needs financing; it builds a hypothesis from observable growth and working-capital signals.</div>
    <div class="warning" id="warning"></div>
  </aside>

  <div class="output">
    <section class="section">
      <div class="section-head"><div><small>01 · Targeting logic</small><h3 id="targetTitle">Inventory Expansion</h3></div><p id="targetDesc">Find ecommerce companies with public evidence suggesting inventory or distribution expansion.</p></div>
      <div class="logic-grid"><div class="logic"><span>Market</span><strong id="logicMarket">United States</strong></div><div class="logic"><span>Business model</span><strong id="logicType">DTC ecommerce brands</strong></div><div class="logic"><span>Primary trigger</span><strong id="logicTrigger">Product / inventory expansion</strong></div><div class="logic"><span>Target volume</span><strong id="logicVolume">500 prospects</strong></div></div>
    </section>

    <section class="section">
      <div class="section-head"><div><small>02 · Live opportunities</small><h3>Accounts with a credible “why now”</h3></div><p>Fit and timing are grounded in public evidence. Click the source behind each signal before using it.</p></div>
      <div class="accounts" id="accounts"><div class="empty">Choose a campaign and run live research.</div></div>
    </section>

    <section class="section">
      <div class="section-head"><div><small>03 · Outbound play</small><h3 id="playHeading">Select an opportunity</h3></div><p>The strongest account becomes the example play. The email uses the same signal that drove account prioritization.</p></div>
      <div class="play-layout">
        <div class="play-summary"><small>RECOMMENDED PLAY</small><h4 id="playTitle">Waiting on live research</h4><p id="playBody">Run a campaign to generate an evidence-backed capital hypothesis.</p><div class="hypothesis"><b>CAPITAL HYPOTHESIS</b><span id="hypothesis">—</span></div></div>
        <div class="message"><div class="message-top"><strong>Email 01 · signal-led</strong><button class="copy" id="copyBtn">Copy email</button></div><div class="subject" id="subject">Subject: —</div><p class="email" id="email">Run a campaign to generate the first live email.</p></div>
      </div>
      <div class="sequence"><div class="touch"><span>DAY 1</span><strong>Email</strong></div><div class="touch"><span>DAY 3</span><strong>LinkedIn</strong></div><div class="touch"><span>DAY 6</span><strong>Email</strong></div><div class="touch"><span>DAY 10</span><strong>Close loop</strong></div></div>
    </section>

    <section class="support">
      <div class="support-card"><small>Delivery plan</small><strong id="deliveryTitle">500 prospects / week</strong><p>Infrastructure scales to the campaign rather than forcing the campaign into whatever sending capacity happens to exist.</p><div class="capacity" id="capacity"><span>3 secondary domains</span><span>9 mailboxes</span><span>SPF / DKIM / DMARC</span></div></div>
      <div class="support-card"><small>Measure</small><strong>Close the loop on the play.</strong><p>Performance data should feed back into targeting so the engine learns which signals and plays create pipeline.</p><div class="pipeline"><b>Send</b><i>→</i><b>Reply</b><i>→</i><b>Positive</b><i>→</i><b>Meeting</b><i>→</i><b>Pipeline</b></div></div>
    </section>
  </div>
</main>

<footer><span>Uncapped Outbound Engine · live prototype</span><span>Public-web signals only · verify before outreach</span></footer>
</div>

<script>
let currentAccounts=[];
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function renderDelivery(){
 const volume=Math.max(100,Number($('volume').value||500));
 const domains=Math.max(2,Math.ceil(volume/180));
 const mailboxes=domains*3;
 $('logicVolume').textContent=volume.toLocaleString()+' prospects';
 $('deliveryTitle').textContent=volume.toLocaleString()+' prospects / week';
 $('capacity').innerHTML=`<span>${domains} secondary domains</span><span>${mailboxes} mailboxes</span><span>SPF / DKIM / DMARC</span>`;
}

function renderAccounts(){
 if(!currentAccounts.length){$('accounts').innerHTML='<div class="empty">No strong evidence-backed accounts found. Try a broader market or another play.</div>';return}
 $('accounts').innerHTML=currentAccounts.map((a,i)=>`<div class="account" onclick="selectAccount(${i})" style="cursor:pointer">
   <div class="score">${esc(a.score)}</div>
   <div class="account-name"><strong>${esc(a.company)}</strong><span>${esc(a.company_description||a.domain||'')}</span><div class="tags">${(a.tags||[]).slice(0,3).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div></div>
   <div class="reason"><small>WHY NOW</small><p>${esc(a.why_now)}</p><a class="evidence" href="${esc(a.source_url)}" target="_blank" rel="noreferrer">${esc(a.source_name||'Evidence')} ↗</a></div>
 </div>`).join('');
}

window.selectAccount=function(i){
 const a=currentAccounts[i]; if(!a)return;
 $('playHeading').textContent=a.play_name||'Outbound play';
 $('playTitle').textContent=a.play_name||'Outbound play';
 $('playBody').textContent=a.uncapped_angle||'';
 $('hypothesis').textContent=a.capital_hypothesis||'';
 $('subject').textContent='Subject: '+(a.email_subject||'');
 $('email').textContent=a.email_body||'';
 document.querySelector('.play-layout').scrollIntoView({behavior:'smooth',block:'center'});
}

async function runCampaign(){
 const btn=$('generate'),warn=$('warning');
 warn.style.display='none';btn.disabled=true;btn.textContent='Researching the market…';
 renderDelivery();
 $('logicMarket').textContent=$('market').value;
 $('logicType').textContent=$('type').value;
 try{
   const res=await fetch('/campaign',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
     goal:$('goal').value,market:$('market').value,company_type:$('type').value,volume:Number($('volume').value||500)
   })});
   const data=await res.json();
   if(!res.ok)throw new Error(data.error||'Campaign research failed');
   $('targetTitle').textContent=data.play_name;
   $('targetDesc').textContent=data.targeting_summary;
   $('logicTrigger').textContent=data.primary_trigger;
   currentAccounts=data.accounts||[];
   renderAccounts();
   if(currentAccounts.length)selectAccount(0);
 }catch(e){
   warn.textContent=e.message;warn.style.display='block';
 }finally{
   btn.disabled=false;btn.textContent='Find live opportunities';
 }
}

$('generate').addEventListener('click',runCampaign);
$('copyBtn').addEventListener('click',async()=>{
 const text=$('subject').textContent+'\n\n'+$('email').textContent;
 await navigator.clipboard.writeText(text);
 const b=$('copyBtn'),old=b.textContent;b.textContent='Copied';setTimeout(()=>b.textContent=old,1000);
});
$('volume').addEventListener('input',renderDelivery);
renderDelivery();
</script>
</body>
</html>"""


def _json_post(url, headers, payload, timeout=60):
    data = json.dumps(payload).encode("utf-8")
    req = urlrequest.Request(url, data=data, headers=headers, method="POST")
    try:
        with urlrequest.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{exc.code}: {body[:350]}")


def tavily_search(query, time_range="month"):
    key = os.environ.get("TAVILY_API_KEY")
    payload = {
        "query": query,
        "search_depth": "basic",
        "topic": "general",
        "time_range": time_range,
        "max_results": 7,
        "include_answer": False,
        "include_raw_content": False,
    }
    return _json_post(
        "https://api.tavily.com/search",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        payload,
        timeout=25,
    ).get("results", [])


def extract_output_text(data):
    if isinstance(data.get("output_text"), str):
        return data["output_text"]
    parts = []
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                parts.append(content["text"])
    return "\n".join(parts)


def build_queries(play, market, company_type):
    terms = " OR ".join(f'"{x}"' for x in play["signal_terms"][:5])
    return [
        f'{company_type} {market} ecommerce brand {terms}',
        f'{company_type} {market} ecommerce "new product" expansion inventory growth',
        f'{company_type} {market} ecommerce Amazon Walmart marketplace expansion',
        f'{company_type} {market} ecommerce growth hiring funding retail expansion',
    ]


def research_market(play, market, company_type):
    raw = []
    for q in build_queries(play, market, company_type):
        raw.extend(tavily_search(q, "month"))

    seen = set()
    unique = []
    for r in raw:
        url = r.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append({
            "title": r.get("title", ""),
            "url": url,
            "snippet": (r.get("content") or "")[:1700],
        })
    return unique[:28]


def output_schema():
    account = {
        "type": "object",
        "properties": {
            "company": {"type": "string"},
            "domain": {"type": "string"},
            "company_description": {"type": "string"},
            "score": {"type": "integer", "minimum": 0, "maximum": 100},
            "tags": {"type": "array", "items": {"type": "string"}},
            "why_now": {"type": "string"},
            "capital_hypothesis": {"type": "string"},
            "uncapped_angle": {"type": "string"},
            "play_name": {"type": "string"},
            "email_subject": {"type": "string"},
            "email_body": {"type": "string"},
            "source_url": {"type": "string"},
            "source_name": {"type": "string"},
        },
        "required": [
            "company","domain","company_description","score","tags","why_now",
            "capital_hypothesis","uncapped_angle","play_name","email_subject",
            "email_body","source_url","source_name"
        ],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "play_name": {"type": "string"},
            "targeting_summary": {"type": "string"},
            "primary_trigger": {"type": "string"},
            "accounts": {"type": "array", "items": account},
        },
        "required": ["play_name","targeting_summary","primary_trigger","accounts"],
        "additionalProperties": False,
    }


def analyze_market(play_key, market, company_type, evidence):
    play = PLAYBOOKS[play_key]
    candidates = [
        {"id": i + 1, "title": x["title"], "url": x["url"], "snippet": x["snippet"]}
        for i, x in enumerate(evidence)
    ]

    prompt = f"""
You are a GTM intelligence analyst building an outbound campaign for Uncapped.

Uncapped provides working and growth capital to ecommerce companies in North America and Europe.

CAMPAIGN
Play: {play["name"]}
Goal: {play["goal"]}
Market: {market}
Company type: {company_type}

PLAY THESIS
{play["thesis"]}

Your job is to identify up to {MAX_RESULTS} REAL ecommerce brands in the supplied web evidence that have a credible, CURRENT reason to be relevant to this Uncapped play.

IMPORTANT:
- Only use companies actually supported by the supplied search evidence.
- Prioritize operating ecommerce brands / merchants, not software vendors, agencies, news publications, investors, marketplaces, or service providers.
- Do NOT claim a company needs financing.
- "Capital hypothesis" must be framed as a hypothesis: explain how the observable event could create a cash-timing or working-capital need.
- Do not invent revenue, inventory levels, ad spend, financing needs, growth rates, or financial distress.
- source_url MUST exactly match one candidate URL below.
- Prefer recent, specific business events over generic company descriptions.
- Dedupe companies.
- If evidence is weak, omit the company.
- Score fit + timing from 0-100.
- 90+: strong ecommerce fit plus a highly relevant current trigger.
- 80-89: strong fit and credible trigger.
- 70-79: plausible but less direct.
- Below 70: omit.

For each account:
- company_description: <= 8 words.
- tags: 2-4 short tags.
- why_now: one concise sentence describing the OBSERVABLE signal.
- capital_hypothesis: one concise sentence connecting the signal to a POSSIBLE working-capital timing issue.
- uncapped_angle: one concise sentence explaining the relevant Uncapped value proposition without assuming they need financing.
- play_name: the best matching outbound play.
- email_subject: 2-5 words.
- email_body: 55-90 words and formatted like a real cold email:
  [First Name],

  short personalized paragraph.

  short capital-timing implication.

  one concise Uncapped sentence.

  low-friction question?

Use blank lines between paragraphs via \\n\\n.
Do not say "based on my research", "I didn't find", "I noticed", "congrats", or narrate your research process.
The email should lead with the specific company event, not Uncapped.

Search evidence:
{json.dumps(candidates, indent=2)}
"""

    data = _json_post(
        "https://api.openai.com/v1/responses",
        {
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        },
        {
            "model": os.environ.get("OPENAI_MODEL", "gpt-5.6-luna"),
            "input": prompt,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "uncapped_outbound_campaign",
                    "strict": True,
                    "schema": output_schema(),
                }
            },
        },
        timeout=90,
    )

    parsed = json.loads(extract_output_text(data))
    allowed = {x["url"] for x in evidence}
    parsed["accounts"] = [
        x for x in parsed.get("accounts", [])
        if x.get("source_url") in allowed and int(x.get("score", 0)) >= 70
    ][:MAX_RESULTS]
    parsed["accounts"].sort(key=lambda x: x.get("score", 0), reverse=True)
    return parsed


@app.get("/")
def home():
    return Response(HTML, mimetype="text/html")


@app.post("/campaign")
def campaign():
    missing = [k for k in ("TAVILY_API_KEY", "OPENAI_API_KEY") if not os.environ.get(k)]
    if missing:
        return jsonify({"error": "Missing Vercel environment variable(s): " + ", ".join(missing)}), 400

    body = request.get_json(silent=True) or {}
    play_key = body.get("goal", "inventory")
    if play_key not in PLAYBOOKS:
        play_key = "inventory"

    market = str(body.get("market", "United States"))[:80]
    company_type = str(body.get("company_type", "DTC ecommerce brands"))[:100]

    try:
        evidence = research_market(PLAYBOOKS[play_key], market, company_type)
        if not evidence:
            return jsonify({"error": "No usable public-web evidence was returned. Try another campaign or market."}), 404

        result = analyze_market(play_key, market, company_type, evidence)
        result["mode"] = "live"
        result["generated_at"] = datetime.now(timezone.utc).isoformat()
        result["sources_scanned"] = len(evidence)
        result["app_version"] = APP_VERSION
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": f"Live campaign research failed: {str(exc)[:550]}"}), 500


@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "app": "uncapped-outbound-engine",
        "version": APP_VERSION,
        "tavily_configured": bool(os.environ.get("TAVILY_API_KEY")),
        "openai_configured": bool(os.environ.get("OPENAI_API_KEY")),
        "model": os.environ.get("OPENAI_MODEL", "gpt-5.6-luna"),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "3000")))
