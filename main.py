from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Uncapped Outbound OS</title>
<meta name="description" content="A prototype outbound operating system built for Uncapped." />
<style>
:root{
  --paper:#f4f1e9;
  --paper-2:#ebe7dc;
  --ink:#111511;
  --ink-2:#1b211c;
  --muted:#687269;
  --line:#d7d2c5;
  --white:#fffdf7;
  --signal:#57e39a;
  --signal-dark:#173f2d;
  --electric:#5d6cff;
  --electric-soft:#e9ebff;
  --warm:#f59a54;
  --warm-soft:#fff0e4;
  --danger:#e56e6e;
  --shadow:0 24px 70px rgba(21,27,22,.10);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
body{min-height:100vh;background:
linear-gradient(rgba(17,21,17,.035) 1px,transparent 1px),
linear-gradient(90deg,rgba(17,21,17,.035) 1px,transparent 1px),
var(--paper);
background-size:32px 32px}
button,input,select{font:inherit}
button{cursor:pointer}
a{color:inherit}
.shell{max-width:1480px;margin:0 auto;padding:24px 28px 70px}

.topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:4px 0 22px;border-bottom:1px solid var(--line);position:relative
}
.brand{display:flex;align-items:center;gap:12px}
.brand-mark{
  width:40px;height:40px;border-radius:50%;background:var(--ink);
  color:var(--signal);display:grid;place-items:center;font-size:20px;font-weight:900;
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)
}
.brand-copy small{display:block;font-size:9px;font-weight:900;letter-spacing:.15em;color:var(--muted)}
.brand-copy strong{font-size:18px;letter-spacing:-.02em}
.nav{display:flex;gap:5px;background:rgba(255,253,247,.7);border:1px solid var(--line);border-radius:999px;padding:4px}
.nav button{
  border:0;background:transparent;color:#697269;padding:8px 12px;border-radius:999px;font-size:10px;font-weight:800
}
.nav button.active{background:var(--ink);color:#fff}
.status{display:flex;gap:8px;align-items:center;font-size:10px;color:var(--muted);font-weight:700}
.status-dot{width:7px;height:7px;border-radius:50%;background:var(--signal);box-shadow:0 0 16px rgba(87,227,154,.75)}

.hero{
  display:grid;grid-template-columns:minmax(0,1.2fr) minmax(360px,.8fr);
  gap:48px;padding:58px 0 40px;align-items:end
}
.kicker{font-size:10px;letter-spacing:.17em;text-transform:uppercase;font-weight:900;color:var(--electric)}
.hero h1{
  font-size:64px;line-height:.97;letter-spacing:-.055em;margin:15px 0 20px;max-width:920px
}
.hero h1 em{font-style:normal;color:var(--signal-dark);position:relative;white-space:nowrap}
.hero h1 em:after{
  content:"";position:absolute;left:0;right:0;bottom:1px;height:10px;background:var(--signal);
  z-index:-1;transform:rotate(-1deg);border-radius:999px;opacity:.72
}
.hero p{font-size:17px;line-height:1.65;color:var(--muted);max-width:780px;margin:0}
.hero-actions{display:flex;gap:9px;margin-top:25px;flex-wrap:wrap}
.primary,.secondary{
  border-radius:12px;padding:12px 16px;font-size:11px;font-weight:900;border:1px solid var(--ink)
}
.primary{background:var(--ink);color:white}
.primary:hover{transform:translateY(-1px)}
.secondary{background:rgba(255,253,247,.75);color:var(--ink);border-color:var(--line)}

.hero-console{
  background:var(--ink);border-radius:28px;padding:19px;color:white;box-shadow:var(--shadow);
  transform:rotate(.4deg);position:relative;overflow:hidden
}
.hero-console:before{
  content:"";position:absolute;width:220px;height:220px;border-radius:50%;
  background:radial-gradient(circle,var(--electric),transparent 65%);right:-90px;top:-100px;opacity:.30
}
.console-top{display:flex;justify-content:space-between;align-items:center;position:relative}
.console-label{font-size:9px;letter-spacing:.13em;font-weight:900;color:#aeb7ae}
.console-badge{font-size:9px;color:var(--signal);border:1px solid rgba(87,227,154,.28);padding:6px 8px;border-radius:999px;background:rgba(87,227,154,.08)}
.console-title{font-size:24px;letter-spacing:-.035em;margin:18px 0 5px;position:relative}
.console-sub{font-size:11px;color:#97a097;line-height:1.5;position:relative}
.console-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:17px;position:relative}
.console-stat{background:#1c231d;border:1px solid #2d352e;border-radius:12px;padding:11px}
.console-stat span{display:block;font-size:8px;color:#8d978e;margin-bottom:5px}
.console-stat strong{font-size:17px}
.signal-green{color:var(--signal)}
.signal-orange{color:var(--warm)}
.console-row{
  margin-top:9px;background:#171d18;border:1px solid #2b332c;border-radius:14px;padding:12px;display:grid;
  grid-template-columns:40px 1fr auto;gap:10px;align-items:center;position:relative
}
.company-icon{width:38px;height:38px;border-radius:10px;background:var(--electric);display:grid;place-items:center;font-size:11px;font-weight:900}
.console-row h4{font-size:11px;margin:0 0 3px}.console-row p{font-size:9px;color:#929c93;margin:0;line-height:1.4}
.row-score{font-size:16px;font-weight:900;color:var(--signal)}

.section-bar{
  display:flex;justify-content:space-between;align-items:end;margin:12px 0 14px
}
.section-bar h2{font-size:27px;letter-spacing:-.035em;margin:4px 0 0}
.section-bar p{font-size:10px;color:var(--muted);max-width:390px;text-align:right;margin:0;line-height:1.5}

.workspace{
  display:grid;grid-template-columns:320px minmax(0,1fr);gap:14px;align-items:start
}
.builder{
  background:var(--white);border:1px solid var(--line);border-radius:22px;padding:17px;box-shadow:0 12px 40px rgba(21,27,22,.05);
  position:sticky;top:16px
}
.builder-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px}
.builder-head strong{font-size:12px}.step{font-size:9px;color:var(--muted)}
.field{margin-bottom:12px}
.field label{display:block;font-size:8.5px;letter-spacing:.11em;text-transform:uppercase;color:#7b817a;font-weight:900;margin-bottom:6px}
.field select,.field input{
  width:100%;border:1px solid var(--line);border-radius:10px;padding:10px;background:#faf8f2;color:var(--ink);outline:none;font-size:11px
}
.field input:focus,.field select:focus{border-color:#9aa2ff;box-shadow:0 0 0 3px rgba(93,108,255,.08)}
.build-btn{
  width:100%;border:0;border-radius:12px;background:var(--electric);color:white;padding:12px;font-size:11px;font-weight:900;margin-top:3px
}
.builder-note{margin-top:11px;font-size:9px;color:#8a9089;line-height:1.45;padding-top:10px;border-top:1px solid var(--line)}

.dashboard{display:flex;flex-direction:column;gap:14px}
.tab-view{display:none}
.tab-view.active{display:block}
.overview-grid{display:grid;grid-template-columns:1.28fr .72fr;gap:14px}
.card{background:var(--white);border:1px solid var(--line);border-radius:22px;padding:18px;box-shadow:0 10px 32px rgba(21,27,22,.045);min-width:0}
.card.dark{background:var(--ink);color:white;border-color:var(--ink)}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:15px;margin-bottom:15px}
.card-head small{font-size:8.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:900;color:#858c85}
.card.dark .card-head small{color:#949d95}
.card-head h3{font-size:17px;letter-spacing:-.025em;margin:4px 0 0}
.link-btn{border:0;background:transparent;color:var(--electric);font-size:9px;font-weight:900;padding:4px}
.card.dark .link-btn{color:var(--signal)}

.account-list{display:flex;flex-direction:column;gap:7px}
.account-row{
  display:grid;grid-template-columns:50px minmax(0,1fr) 105px 70px;gap:10px;align-items:center;
  border:1px solid #e4dfd3;border-radius:14px;padding:10px;background:#fcfaf4
}
.account-score{
  width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:var(--signal-dark);color:var(--signal);
  font-size:13px;font-weight:900
}
.account-name strong{display:block;font-size:11px;margin-bottom:2px}.account-name span{font-size:9px;color:var(--muted)}
.signal-type{font-size:8.5px;font-weight:850;text-align:center;padding:6px;border-radius:999px;background:var(--electric-soft);color:#414ca7}
.heat{font-size:9px;font-weight:900;text-align:right}
.heat.hot{color:#137f59}.heat.warm{color:#b66621}

.play-card{background:#181f19;border:1px solid #2a322b;border-radius:16px;padding:14px;margin-top:9px}
.play-label{font-size:8px;color:var(--signal);font-weight:900;letter-spacing:.12em}
.play-card h4{font-size:15px;margin:7px 0 5px}.play-card p{font-size:10px;color:#a3ada4;line-height:1.5;margin:0}
.play-meta{display:flex;gap:5px;flex-wrap:wrap;margin-top:11px}
.play-meta span{border:1px solid #303b31;background:#1f2720;border-radius:999px;padding:5px 7px;font-size:8px;color:#aeb7af}

.triple{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.metric{min-height:154px}
.metric-top{display:flex;justify-content:space-between;align-items:center}
.metric small{font-size:8px;color:var(--muted);font-weight:900;letter-spacing:.1em}
.metric .big{font-size:32px;letter-spacing:-.045em;font-weight:900;margin:22px 0 5px}
.metric p{font-size:9.5px;color:var(--muted);line-height:1.45;margin:0}
.spark{display:flex;align-items:end;gap:3px;height:30px;margin-top:14px}
.spark i{display:block;width:8%;border-radius:3px 3px 0 0;background:var(--signal)}
.spark i:nth-child(2n){background:var(--electric)}
.spark i:nth-child(3n){background:var(--warm)}

.infra-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.health-stack{display:flex;flex-direction:column;gap:8px}
.health-row{display:grid;grid-template-columns:1fr auto;gap:12px;border-bottom:1px solid var(--line);padding:8px 0}
.health-row:last-child{border-bottom:0}
.health-row strong{font-size:10.5px}.health-row span{display:block;font-size:8.5px;color:var(--muted);margin-top:2px}
.health-pill{font-size:8px;font-weight:900;padding:6px 7px;border-radius:999px;align-self:center}
.good{background:var(--signal);color:#123c2a}.warn{background:var(--warm-soft);color:#a15b1d}.risk{background:#fde7e7;color:#9d3f3f}

.capacity{
  display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:10px
}
.capacity div{background:#f8f5ee;border:1px solid var(--line);border-radius:11px;padding:9px}
.capacity span{display:block;font-size:8px;color:var(--muted);margin-bottom:4px}
.capacity strong{font-size:15px}

.flow{display:grid;grid-template-columns:repeat(5,1fr);gap:7px;margin-top:12px}
.flow-step{background:#191f1a;border:1px solid #2c342d;border-radius:12px;padding:10px;position:relative}
.flow-step span{display:block;font-size:8px;color:#8f9990}.flow-step strong{font-size:13px;display:block;margin-top:5px}
.flow-step:after{content:"→";position:absolute;right:-7px;top:50%;transform:translateY(-50%);color:#5d665e}
.flow-step:last-child:after{display:none}

.performance-table{width:100%;border-collapse:separate;border-spacing:0 6px}
.performance-table th{font-size:8px;text-align:left;color:#868d86;padding:0 9px 3px;text-transform:uppercase;letter-spacing:.08em}
.performance-table td{background:#faf8f2;border-top:1px solid #e5e0d5;border-bottom:1px solid #e5e0d5;padding:10px 9px;font-size:9.5px}
.performance-table td:first-child{border-left:1px solid #e5e0d5;border-radius:10px 0 0 10px;font-weight:850}
.performance-table td:last-child{border-right:1px solid #e5e0d5;border-radius:0 10px 10px 0}
.delta{font-weight:900;color:#168158}
.rec{
  margin-top:12px;background:var(--signal-dark);color:#daf9e8;border-radius:14px;padding:13px;display:grid;
  grid-template-columns:34px 1fr;gap:10px;align-items:start
}
.rec-icon{width:32px;height:32px;border-radius:9px;background:var(--signal);color:var(--signal-dark);display:grid;place-items:center;font-weight:900}
.rec strong{font-size:10.5px}.rec p{font-size:9px;color:#abd8bd;margin:4px 0 0;line-height:1.5}

.mini-footer{
  margin-top:40px;border-top:1px solid var(--line);padding-top:18px;display:flex;justify-content:space-between;gap:20px;
  font-size:9px;color:#8b918b
}

@media(max-width:1050px){
  .hero{grid-template-columns:1fr}.hero-console{transform:none;max-width:680px}
  .workspace{grid-template-columns:1fr}.builder{position:static}
  .overview-grid,.infra-grid{grid-template-columns:1fr}
}
@media(max-width:760px){
  .shell{padding:18px 12px 45px}.nav{display:none}.hero{padding-top:38px}.hero h1{font-size:44px}
  .triple{grid-template-columns:1fr}.account-row{grid-template-columns:48px 1fr}.signal-type,.heat{grid-column:2;text-align:left;width:max-content}
  .capacity{grid-template-columns:1fr 1fr}.flow{grid-template-columns:1fr}.flow-step:after{display:none}
  .section-bar{display:block}.section-bar p{text-align:left;margin-top:8px}
}
</style>
</head>
<body>
<div class="shell">
  <header class="topbar">
    <div class="brand">
      <div class="brand-mark">u</div>
      <div class="brand-copy">
        <small>BUILT FOR UNCAPPED</small>
        <strong>Outbound OS</strong>
      </div>
    </div>

    <nav class="nav">
      <button class="active" data-tab="opportunities">Opportunities</button>
      <button data-tab="plays">Plays</button>
      <button data-tab="infrastructure">Infrastructure</button>
      <button data-tab="performance">Performance</button>
    </nav>

    <div class="status"><span class="status-dot"></span> prototype online</div>
  </header>

  <section class="hero">
    <div>
      <div class="kicker">Signals → Plays → Sends → Pipeline</div>
      <h1>Turn fragmented outbound into a <em>real engine.</em></h1>
      <p>
        A working concept for how Uncapped could unify account signals, targeting, outbound plays,
        sending infrastructure and funnel analytics into one operator layer.
      </p>
      <div class="hero-actions">
        <button class="primary" onclick="document.getElementById('workspace').scrollIntoView()">Build a campaign</button>
        <button class="secondary" onclick="switchTab('infrastructure')">See infrastructure health</button>
      </div>
    </div>

    <aside class="hero-console">
      <div class="console-top">
        <span class="console-label">TODAY'S OUTBOUND PULSE</span>
        <span class="console-badge">● systems healthy</span>
      </div>
      <div class="console-title">12 accounts moved into high intent.</div>
      <div class="console-sub">Signals are ranked by fit, capital need and timing — then routed into the right outbound play.</div>

      <div class="console-grid">
        <div class="console-stat"><span>HIGH INTENT</span><strong class="signal-green">12</strong></div>
        <div class="console-stat"><span>SAFE CAPACITY</span><strong>1,820</strong></div>
        <div class="console-stat"><span>MEETINGS / 7D</span><strong class="signal-orange">19</strong></div>
      </div>

      <div class="console-row">
        <div class="company-icon">N</div>
        <div><h4>Nutripaw</h4><p>Inventory expansion + marketplace growth</p></div>
        <div class="row-score">94</div>
      </div>
      <div class="console-row">
        <div class="company-icon" style="background:var(--warm)">S</div>
        <div><h4>Skin + Me</h4><p>Growth hiring + paid acquisition signal</p></div>
        <div class="row-score">91</div>
      </div>
    </aside>
  </section>

  <div class="section-bar">
    <div>
      <div class="kicker">THE OPERATOR LAYER</div>
      <h2>Everything outbound should work through one system.</h2>
    </div>
    <p>Prototype data below is illustrative. The point is the operating model: target, route, send, measure, improve.</p>
  </div>

  <section class="workspace" id="workspace">
    <aside class="builder">
      <div class="builder-head"><strong>Build me a campaign</strong><span class="step">01 / 03</span></div>

      <div class="field">
        <label>Goal</label>
        <select id="goal">
          <option>Acquire high-growth ecommerce brands</option>
          <option>Expand Amazon seller segment</option>
          <option>Target inventory-heavy brands</option>
          <option>Target marketplace expansion</option>
        </select>
      </div>

      <div class="field">
        <label>Region</label>
        <select id="region">
          <option>United States</option>
          <option>United Kingdom</option>
          <option>North America</option>
          <option>Europe</option>
        </select>
      </div>

      <div class="field">
        <label>Trigger</label>
        <select id="trigger">
          <option>Inventory / product expansion</option>
          <option>Marketplace expansion</option>
          <option>Growth hiring</option>
          <option>Funding / growth event</option>
          <option>Paid acquisition growth</option>
        </select>
      </div>

      <div class="field">
        <label>Weekly volume</label>
        <input id="volume" type="number" value="1800" min="100" max="10000" />
      </div>

      <button class="build-btn" id="buildBtn">Generate outbound plan</button>
      <div class="builder-note">
        This prototype treats infrastructure as part of the campaign design — not an afterthought.
      </div>
    </aside>

    <div class="dashboard">

      <div class="tab-view active" id="tab-opportunities">
        <div class="overview-grid">
          <div class="card">
            <div class="card-head">
              <div><small>OPPORTUNITIES</small><h3>Accounts worth working now</h3></div>
              <button class="link-btn">View all 38 →</button>
            </div>

            <div class="account-list">
              <div class="account-row">
                <div class="account-score">94</div>
                <div class="account-name"><strong>Nutripaw</strong><span>Pet wellness · ecommerce</span></div>
                <div class="signal-type">Inventory expansion</div>
                <div class="heat hot">HOT</div>
              </div>
              <div class="account-row">
                <div class="account-score">91</div>
                <div class="account-name"><strong>Skin + Me</strong><span>Beauty subscription · DTC</span></div>
                <div class="signal-type">Growth hiring</div>
                <div class="heat hot">HOT</div>
              </div>
              <div class="account-row">
                <div class="account-score">88</div>
                <div class="account-name"><strong>Freja</strong><span>Furniture · ecommerce</span></div>
                <div class="signal-type">Marketplace growth</div>
                <div class="heat warm">HIGH</div>
              </div>
              <div class="account-row">
                <div class="account-score">84</div>
                <div class="account-name"><strong>Spoke</strong><span>Apparel · DTC</span></div>
                <div class="signal-type">New product cycle</div>
                <div class="heat warm">HIGH</div>
              </div>
            </div>
          </div>

          <div class="card dark">
            <div class="card-head">
              <div><small>RECOMMENDED PLAY</small><h3>Inventory Expansion</h3></div>
              <button class="link-btn" onclick="switchTab('plays')">Open play →</button>
            </div>

            <div class="play-card">
              <div class="play-label">WHY NOW</div>
              <h4>Working capital before the revenue lands.</h4>
              <p>Use product launches, new categories and marketplace expansion to identify brands likely funding inventory ahead of cash conversion.</p>
              <div class="play-meta">
                <span>CFO / Founder</span>
                <span>US ecommerce</span>
                <span>Physical inventory</span>
              </div>
            </div>

            <div class="flow">
              <div class="flow-step"><span>DAY 1</span><strong>Email</strong></div>
              <div class="flow-step"><span>DAY 3</span><strong>LinkedIn</strong></div>
              <div class="flow-step"><span>DAY 6</span><strong>Email</strong></div>
              <div class="flow-step"><span>DAY 10</span><strong>Email</strong></div>
              <div class="flow-step"><span>DAY 14</span><strong>Close loop</strong></div>
            </div>
          </div>
        </div>

        <div class="triple" style="margin-top:14px">
          <div class="card metric">
            <div class="metric-top"><small>FIT + INTENT</small><span class="signal-type">↑ 18%</span></div>
            <div class="big">38</div>
            <p>Accounts currently above the high-intent threshold.</p>
            <div class="spark"><i style="height:28%"></i><i style="height:45%"></i><i style="height:37%"></i><i style="height:55%"></i><i style="height:48%"></i><i style="height:68%"></i><i style="height:59%"></i><i style="height:82%"></i><i style="height:73%"></i></div>
          </div>
          <div class="card metric">
            <div class="metric-top"><small>SEND CAPACITY</small><span class="signal-type">Healthy</span></div>
            <div class="big">1,820</div>
            <p>Safe weekly volume based on current mailbox health.</p>
            <div class="spark"><i style="height:40%"></i><i style="height:41%"></i><i style="height:44%"></i><i style="height:52%"></i><i style="height:56%"></i><i style="height:61%"></i><i style="height:67%"></i><i style="height:72%"></i><i style="height:77%"></i></div>
          </div>
          <div class="card metric">
            <div class="metric-top"><small>MEETING RATE</small><span class="signal-type">Best play</span></div>
            <div class="big">2.7%</div>
            <p>Inventory Expansion currently leads all outbound plays.</p>
            <div class="spark"><i style="height:22%"></i><i style="height:31%"></i><i style="height:29%"></i><i style="height:42%"></i><i style="height:39%"></i><i style="height:54%"></i><i style="height:48%"></i><i style="height:64%"></i><i style="height:71%"></i></div>
          </div>
        </div>
      </div>

      <div class="tab-view" id="tab-plays">
        <div class="overview-grid">
          <div class="card dark">
            <div class="card-head"><div><small>PLAY 01</small><h3>Inventory Expansion</h3></div><span class="console-badge">Highest meeting rate</span></div>
            <div class="play-card">
              <div class="play-label">TRIGGER</div>
              <h4>New product lines, categories or marketplace launches.</h4>
              <p>Hypothesis: the brand may need to fund more inventory before the related customer revenue is realized.</p>
            </div>
            <div class="play-card">
              <div class="play-label">MESSAGE ANGLE</div>
              <h4>Fund the growth cycle — not the waiting period.</h4>
              <p>Lead with the commercial event, connect it to working-capital timing, then position Uncapped as flexible capital designed around ecommerce cash flow.</p>
            </div>
          </div>

          <div class="card">
            <div class="card-head"><div><small>ROUTING LOGIC</small><h3>Who enters this play</h3></div></div>
            <div class="health-stack">
              <div class="health-row"><div><strong>Physical inventory</strong><span>Brand carries or finances goods</span></div><div class="health-pill good">Required</div></div>
              <div class="health-row"><div><strong>Growth signal</strong><span>Launch, expansion or marketplace event</span></div><div class="health-pill good">Required</div></div>
              <div class="health-row"><div><strong>Revenue fit</strong><span>Meets Uncapped qualification band</span></div><div class="health-pill good">Required</div></div>
              <div class="health-row"><div><strong>Capital timing</strong><span>Inventory before cash conversion</span></div><div class="health-pill warn">Inferred</div></div>
            </div>
          </div>
        </div>

        <div class="triple" style="margin-top:14px">
          <div class="card"><div class="card-head"><div><small>PLAY 02</small><h3>Paid Growth</h3></div></div><p style="font-size:10px;color:var(--muted);line-height:1.6;margin:0">Target brands scaling acquisition where marketing spend lands before the customer cash does.</p></div>
          <div class="card"><div class="card-head"><div><small>PLAY 03</small><h3>Marketplace Expansion</h3></div></div><p style="font-size:10px;color:var(--muted);line-height:1.6;margin:0">Use new Amazon or Walmart expansion as a working-capital trigger around inventory and payout cycles.</p></div>
          <div class="card"><div class="card-head"><div><small>PLAY 04</small><h3>Seasonality</h3></div></div><p style="font-size:10px;color:var(--muted);line-height:1.6;margin:0">Identify businesses building inventory ahead of peak periods or responding to short-lived product demand.</p></div>
        </div>
      </div>

      <div class="tab-view" id="tab-infrastructure">
        <div class="infra-grid">
          <div class="card">
            <div class="card-head"><div><small>SENDING INFRASTRUCTURE</small><h3>Mailbox health</h3></div><span class="signal-type">24 active</span></div>
            <div class="health-stack">
              <div class="health-row"><div><strong>jake@tryuncapped.co</strong><span>SPF ✓ · DKIM ✓ · DMARC ✓</span></div><div class="health-pill good">94</div></div>
              <div class="health-row"><div><strong>sarah@getuncapped.co</strong><span>SPF ✓ · DKIM ✓ · DMARC ✓</span></div><div class="health-pill good">91</div></div>
              <div class="health-row"><div><strong>matt@uncappedcapital.co</strong><span>Inbox placement trending down</span></div><div class="health-pill warn">72</div></div>
              <div class="health-row"><div><strong>alex@meetuncapped.co</strong><span>Bounce rate above target</span></div><div class="health-pill risk">61</div></div>
            </div>
          </div>

          <div class="card dark">
            <div class="card-head"><div><small>CAPACITY MODEL</small><h3>Safe sending architecture</h3></div></div>
            <p style="font-size:10px;color:#a2aca3;line-height:1.55;margin:0">Capacity should be determined by mailbox health and placement — not by the volume target alone.</p>
            <div class="capacity">
              <div><span>DOMAINS</span><strong>8</strong></div>
              <div><span>MAILBOXES</span><strong>24</strong></div>
              <div><span>/ MAILBOX / DAY</span><strong>15</strong></div>
              <div><span>WEEKLY SAFE</span><strong>1,820</strong></div>
            </div>
            <div class="rec">
              <div class="rec-icon">!</div>
              <div><strong>Rebalance before scaling.</strong><p>Reduce volume on two weaker mailboxes and shift capacity toward domains maintaining strong placement.</p></div>
            </div>
          </div>
        </div>

        <div class="triple" style="margin-top:14px">
          <div class="card metric"><div class="metric-top"><small>INBOX PLACEMENT</small><span class="health-pill good">Healthy</span></div><div class="big">91%</div><p>Weighted across active sending domains.</p></div>
          <div class="card metric"><div class="metric-top"><small>BOUNCE RATE</small><span class="health-pill good">Target</span></div><div class="big">1.3%</div><p>Below the current guardrail.</p></div>
          <div class="card metric"><div class="metric-top"><small>DOMAIN UTILIZATION</small><span class="health-pill warn">Watch</span></div><div class="big">68%</div><p>Enough headroom to scale selectively.</p></div>
        </div>
      </div>

      <div class="tab-view" id="tab-performance">
        <div class="card">
          <div class="card-head"><div><small>FULL-FUNNEL PERFORMANCE</small><h3>From send → meeting</h3></div><button class="link-btn">Last 30 days ▾</button></div>
          <table class="performance-table">
            <thead><tr><th>Play</th><th>Sent</th><th>Replies</th><th>Positive</th><th>Meetings</th><th>Meeting rate</th></tr></thead>
            <tbody>
              <tr><td>Inventory Expansion</td><td>1,240</td><td>84</td><td>29</td><td>14</td><td class="delta">2.7%</td></tr>
              <tr><td>Marketplace Growth</td><td>840</td><td>43</td><td>14</td><td>8</td><td>1.7%</td></tr>
              <tr><td>Paid Growth</td><td>950</td><td>38</td><td>12</td><td>6</td><td>1.3%</td></tr>
              <tr><td>Generic Ecommerce</td><td>1,115</td><td>27</td><td>7</td><td>3</td><td>.6%</td></tr>
            </tbody>
          </table>
          <div class="rec">
            <div class="rec-icon">↗</div>
            <div><strong>Shift volume toward Inventory Expansion.</strong><p>It is currently producing the strongest meeting rate and positive-reply efficiency. Reduce generic volume and allocate more healthy mailbox capacity to this play.</p></div>
          </div>
        </div>

        <div class="triple" style="margin-top:14px">
          <div class="card metric"><div class="metric-top"><small>TOTAL SENDS</small></div><div class="big">4,145</div><p>Across all outbound plays.</p></div>
          <div class="card metric"><div class="metric-top"><small>POSITIVE REPLIES</small></div><div class="big">62</div><p>Qualified positive intent generated.</p></div>
          <div class="card metric"><div class="metric-top"><small>MEETINGS</small></div><div class="big">31</div><p>Outbound-sourced meetings booked.</p></div>
        </div>
      </div>

    </div>
  </section>

  <div class="mini-footer">
    <span>Outbound OS · concept built for Uncapped</span>
    <span>Illustrative prototype data · not connected to Uncapped systems</span>
  </div>
</div>

<script>
const navButtons=[...document.querySelectorAll('[data-tab]')];
function switchTab(name){
  document.querySelectorAll('.tab-view').forEach(v=>v.classList.remove('active'));
  const target=document.getElementById('tab-'+name);
  if(target) target.classList.add('active');
  navButtons.forEach(b=>b.classList.toggle('active',b.dataset.tab===name));
  document.getElementById('workspace').scrollIntoView({behavior:'smooth',block:'start'});
}
window.switchTab=switchTab;
navButtons.forEach(b=>b.addEventListener('click',()=>switchTab(b.dataset.tab)));

document.getElementById('buildBtn').addEventListener('click',()=>{
  const btn=document.getElementById('buildBtn');
  const volume=Math.max(100,Number(document.getElementById('volume').value||1800));
  const old=btn.textContent;
  btn.textContent='Building plan…';
  btn.disabled=true;
  setTimeout(()=>{
    btn.textContent=`Plan ready for ${volume.toLocaleString()} / week`;
    switchTab('opportunities');
    setTimeout(()=>{btn.textContent=old;btn.disabled=false},1800);
  },650);
});
</script>
</body>
</html>"""

@app.get("/")
def home():
    return Response(HTML, mimetype="text/html")

@app.get("/health")
def health():
    return {"ok": True, "app": "uncapped-outbound-os", "version": "landing-v1"}

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "3000")))
