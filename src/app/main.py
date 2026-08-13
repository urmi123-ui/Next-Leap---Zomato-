import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from app.models.domain import UserPreferences, RecommendationResponse

st.set_page_config(
    page_title="Zomato – AI Restaurant Recommendations",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def get_restaurant_image(cuisines: list, name: str) -> str:
    cuisines_lower = [c.lower() for c in cuisines]
    name_lower = name.lower()
    if any("biryani" in c for c in cuisines_lower) or "biryani" in name_lower:
        return "https://lh3.googleusercontent.com/aida-public/AB6AXuC4bGymiW8kqdTxzu3T_CU9pu7D5gqIF0Cgq5S-TpxF5xurvukJ_LU0Kav4IEAcKi55sHsVaB3O9IzjJgNW5g4iwXYwcv3grpYz3bC320qzkI2GE-Jg6IwOuYmFyNfevogdHszsOXxgcZ86KBW7KXVf2cUX8bbculcnPSCrN1RkbBS4Tm16vo4_FMlIk4u7yDPhYECqv6cekKdEWuMHyqgBqo3WlyBa96FCpQNdl-_lO47VsOOCxyye"
    if any("south indian" in c for c in cuisines_lower) or "andhra" in name_lower or "dosa" in name_lower:
        return "https://lh3.googleusercontent.com/aida-public/AB6AXuD9b5EwnilJ8TyfeyjcCXv0vSqPUVL0TMrSS3U0YH7biyOi8fOeRc1yKUjjyRM8lhsv0abCUp55p0R7evnMYtipcGligDWDR9_WXWtz-KQvjHvRYBw1Ea5C8TcRoU2JRuTRJkMQjJ6vP1UwhWA4-7n6-Md5dz-JGVv2kmOecsfe5dtmiRnP-QD4LjuKQ2MSBOIeIiUbVIG_yCkJnK2wjSeZqB4rWmjPwxMOEeBlOFIaGRJj98RmibS3"
    if any(x in cuisines_lower for x in ["ramen", "japanese", "korean", "thai"]):
        return "https://lh3.googleusercontent.com/aida-public/AB6AXuDAHHh2mRlfVHjTTnjuZEz1ih6F2G7aXv5EoLT-i9bOFyZ-jrpPxs3mvJqNwRZnJO796PUXZ4KTco3REtpCztmr5EkCaGIbAVcERLuVc93cV0W5zu-6MvigU5HhfVqHlDf9WDOqdfbeHE8Fb3dbP34w9wpo121AWyG_4t4WO-4vCRlUmq4JFvDwKfHnd_slXIW3GFVIs8HD3VmqFMfruxK67TKtu4JxLR7fZDiBMNYl_U1o_gkt9wbY"
    if any(x in cuisines_lower for x in ["chinese", "asian", "continental"]):
        return "https://lh3.googleusercontent.com/aida-public/AB6AXuAhKPs_zhJ09ZTiWmgLNNgFJMRa0Cmcl5pchdPAs4ibjQKZwm2hjRQeF6DvGNMLv3dTy8AAx0lqVdSqUh451EPu7TQDsm4Pc78uFl18bEiiQuENUtOZ-OJ8iivTupB5iBvqgyregy50z37Mt6-3fiblf4595KGyI1M7gfZVLPlmc3m2G99uuwI0q7wurpLcRknw0I7Dq_hErpccyQdH7B5xtzfm_xHugK_Ny2rEnL-a-zUSv2JrfZVA"
    if any(x in cuisines_lower for x in ["italian", "pizza", "pasta"]):
        return "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&q=80&w=600"
    if any(x in cuisines_lower for x in ["cafe", "coffee", "desserts", "fast food", "burger"]):
        return "https://images.unsplash.com/photo-1498804103079-a6351b050096?auto=format&fit=crop&q=80&w=600"
    return "https://lh3.googleusercontent.com/aida-public/AB6AXuDvw3j7rQQ6gG4_yZ_bvSwA3JbTA5B0dN6Va-xHiu2MbUZsBsD6Pa3xfYXynZx-BcZ99O4hUV7rUs9FImjGSXi5Q3b4xJYJMdetQjeK0EmkJaU6aljUL7_xikWWExZnsXoQY-einT_ahqKgCIb2balfs19c5lH4uZznyIgpikdueTeUbqeHewsonede6gPw2QRWjgr3eRMzH_CkrE9S9C07tw8BodCz1bn9ebx6Miqh2XFZ95aam-WR"

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],.stApp,.main,section.main{
  background:#0a0a0a!important;color:#f0f0f0!important;
  font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif!important;}
#MainMenu,footer,[data-testid="stHeader"],[data-testid="stToolbar"],.stDeployButton{display:none!important;}
[data-testid="stSidebar"]{display:none!important;}
[data-testid="stAppViewBlockContainer"],.block-container{padding:0!important;max-width:100%!important;}
::-webkit-scrollbar{width:6px;}
::-webkit-scrollbar-track{background:#111;}
::-webkit-scrollbar-thumb{background:#E23744;border-radius:3px;}

/* NAV */
.zomato-nav{position:fixed;top:0;left:0;right:0;z-index:9999;display:flex;align-items:center;
  justify-content:space-between;padding:0 40px;height:64px;
  background:rgba(10,10,10,0.9);backdrop-filter:blur(20px);
  border-bottom:1px solid rgba(255,255,255,0.07);}
.nav-logo{width:38px;height:38px;background:linear-gradient(135deg,#E23744,#c0202e);
  border-radius:10px;display:flex;align-items:center;justify-content:center;
  font-size:20px;box-shadow:0 4px 18px rgba(226,55,68,0.45);flex-shrink:0;}
.nav-name{font-size:22px;font-weight:900;color:#fff;letter-spacing:-0.5px;margin-left:10px;}
.nav-name em{color:#E23744;font-style:normal;}
.nav-beta{font-size:10px;font-weight:700;color:#E23744;background:rgba(226,55,68,0.12);
  border:1px solid rgba(226,55,68,0.3);border-radius:20px;padding:2px 9px;
  letter-spacing:1.2px;text-transform:uppercase;margin-left:10px;}
.nav-city{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:500;color:#aaa;
  background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.09);
  border-radius:20px;padding:6px 14px;}
.nav-avatar{width:36px;height:36px;background:linear-gradient(135deg,#E23744,#ff6b6b);
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:14px;font-weight:800;color:#fff;margin-left:12px;cursor:pointer;
  transition:transform .2s,box-shadow .2s;}
.nav-avatar:hover{transform:scale(1.1);box-shadow:0 0 0 3px rgba(226,55,68,.35);}

/* HERO */
.hero{position:relative;overflow:hidden;padding:90px 40px 64px;text-align:center;background:#0a0a0a;}
.hero-glow{position:absolute;top:-120px;left:50%;transform:translateX(-50%);width:900px;height:600px;
  background:radial-gradient(ellipse at center,rgba(226,55,68,.16) 0%,transparent 65%);pointer-events:none;}
.hero-pill{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:700;
  color:#E23744;text-transform:uppercase;letter-spacing:2px;
  background:rgba(226,55,68,.1);border:1px solid rgba(226,55,68,.25);
  border-radius:20px;padding:6px 16px;margin-bottom:26px;}
.hero-h1{font-size:clamp(42px,6vw,74px);font-weight:900;color:#fff;line-height:1.04;
  letter-spacing:-2.5px;margin-bottom:22px;}
.hero-h1 .red{background:linear-gradient(135deg,#E23744,#ff8f6b);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:17px;font-weight:400;color:#777;max-width:520px;margin:0 auto 44px;line-height:1.65;}
.hero-stats{display:flex;justify-content:center;gap:48px;flex-wrap:wrap;}
.stat-num{font-size:30px;font-weight:900;color:#fff;line-height:1;}
.stat-lbl{font-size:11px;font-weight:600;color:#555;margin-top:4px;text-transform:uppercase;letter-spacing:1.2px;}
.stat-divider{width:1px;height:40px;background:rgba(255,255,255,.09);margin:auto 0;}

/* MAIN WRAPPER */
.page-top{padding-top:64px;}
.wrap{padding:0 40px 40px;max-width:1400px;margin:0 auto;}

/* STATUS BARS */
.bar-err{display:flex;align-items:center;gap:12px;background:rgba(226,55,68,.08);
  border:1px solid rgba(226,55,68,.25);border-radius:12px;padding:14px 20px;
  margin-bottom:24px;font-size:14px;color:#ff8888;}
.bar-ok{display:flex;align-items:center;gap:12px;background:rgba(34,197,94,.07);
  border:1px solid rgba(34,197,94,.2);border-radius:12px;padding:14px 20px;
  margin-bottom:24px;font-size:14px;color:#86efac;}
.bar-info{display:flex;align-items:center;gap:12px;background:rgba(99,179,237,.07);
  border:1px solid rgba(99,179,237,.2);border-radius:12px;padding:14px 20px;
  margin-bottom:24px;font-size:14px;color:#93c5fd;}

/* PREFS CARD */
.prefs-card{background:linear-gradient(145deg,#141414,#111);border:1px solid rgba(255,255,255,.08);
  border-radius:20px;padding:32px;margin-bottom:32px;position:relative;overflow:hidden;}
.prefs-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,#E23744,#ff8f6b,transparent);}
.prefs-title{font-size:19px;font-weight:800;color:#fff;display:flex;align-items:center;
  gap:10px;margin-bottom:6px;}
.prefs-icon{width:32px;height:32px;background:linear-gradient(135deg,#E23744,#c0202e);
  border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;}
.prefs-sub{font-size:13px;color:#555;margin-bottom:28px;}

/* WIDGET OVERRIDES */
.stSelectbox label,.stSlider label,.stTextInput label,.stRadio label,
.stSelectbox [data-testid="stWidgetLabel"],.stSlider [data-testid="stWidgetLabel"],
.stTextInput [data-testid="stWidgetLabel"],.stRadio [data-testid="stWidgetLabel"]{
  font-size:11px!important;font-weight:700!important;color:#666!important;
  text-transform:uppercase!important;letter-spacing:1.2px!important;
  margin-bottom:8px!important;font-family:'Inter',sans-serif!important;}
div[data-baseweb="select"]>div{background:#1c1c1c!important;border:1px solid rgba(255,255,255,.1)!important;
  border-radius:12px!important;color:#f0f0f0!important;font-family:'Inter',sans-serif!important;}
div[data-baseweb="select"]>div:hover{border-color:#E23744!important;}
div[data-baseweb="select"]>div:focus-within{border-color:#E23744!important;box-shadow:0 0 0 3px rgba(226,55,68,.15)!important;}
div[data-baseweb="select"] span{color:#f0f0f0!important;}
[data-baseweb="select"] svg{fill:#777!important;}
.stTextInput input{background:#1c1c1c!important;border:1px solid rgba(255,255,255,.1)!important;
  border-radius:12px!important;color:#f0f0f0!important;font-family:'Inter',sans-serif!important;
  font-size:14px!important;padding:10px 16px!important;}
.stTextInput input:focus{border-color:#E23744!important;box-shadow:0 0 0 3px rgba(226,55,68,.15)!important;}
.stTextInput input::placeholder{color:#444!important;}
div[data-testid="stRadio"] div[role="radiogroup"]{display:flex!important;flex-direction:row!important;
  background:#1c1c1c!important;border:1px solid rgba(255,255,255,.1)!important;
  border-radius:12px!important;overflow:hidden!important;padding:0!important;}
div[data-testid="stRadio"] div[role="radiogroup"]>label{flex:1!important;text-align:center!important;
  padding:10px 16px!important;margin:0!important;color:#777!important;font-weight:600!important;
  font-size:13px!important;cursor:pointer!important;transition:all .2s!important;
  border-right:1px solid rgba(255,255,255,.07)!important;}
div[data-testid="stRadio"] div[role="radiogroup"]>label:last-child{border-right:none!important;}
div[data-testid="stRadio"] div[role="radiogroup"] [data-checked="true"]{
  background:linear-gradient(135deg,#E23744,#c0202e)!important;color:#fff!important;}
div[data-testid="stRadio"] div[role="radiogroup"] input[type="radio"]{display:none!important;}
div[data-testid="stRadio"] div[role="radiogroup"] [data-testid="stMarkdownContainer"] p{
  margin:0!important;font-weight:inherit!important;color:inherit!important;}
.stSlider [role="slider"]{background:#E23744!important;border:2px solid #E23744!important;
  box-shadow:0 0 12px rgba(226,55,68,.5)!important;}
div.stButton>button{background:linear-gradient(135deg,#E23744,#c0202e)!important;color:#fff!important;
  font-size:15px!important;font-weight:700!important;font-family:'Inter',sans-serif!important;
  padding:14px 48px!important;border-radius:14px!important;border:none!important;
  box-shadow:0 8px 30px rgba(226,55,68,.35)!important;
  transition:all .25s cubic-bezier(.34,1.56,.64,1)!important;
  width:auto!important;display:block!important;margin:0 auto!important;}
div.stButton>button:hover{transform:translateY(-3px) scale(1.02)!important;
  box-shadow:0 16px 44px rgba(226,55,68,.5)!important;}
div.stButton>button:disabled{background:#222!important;box-shadow:none!important;
  color:#444!important;cursor:not-allowed!important;transform:none!important;}
div.stButton>button p{color:#fff!important;font-weight:700!important;}
div[data-baseweb="popover"]{background:#1c1c1c!important;border:1px solid rgba(255,255,255,.1)!important;
  border-radius:12px!important;box-shadow:0 20px 60px rgba(0,0,0,.6)!important;}
div[data-baseweb="popover"] ul{background:#1c1c1c!important;border:none!important;}
div[data-baseweb="popover"] li{color:#f0f0f0!important;background:#1c1c1c!important;
  font-family:'Inter',sans-serif!important;font-size:14px!important;}
div[data-baseweb="popover"] li:hover{background:rgba(226,55,68,.12)!important;color:#E23744!important;}
div[data-baseweb="popover"] li[aria-selected="true"]{background:rgba(226,55,68,.2)!important;
  color:#E23744!important;font-weight:600!important;}
[data-testid="column"]{padding:0 8px!important;}

/* RESULTS */
.results-hdr{display:flex;align-items:center;justify-content:space-between;
  margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,.07);}
.results-ttl{font-size:22px;font-weight:800;color:#fff;}
.results-badge{font-size:12px;font-weight:700;color:#E23744;
  background:rgba(226,55,68,.12);border:1px solid rgba(226,55,68,.25);
  border-radius:20px;padding:4px 14px;}

/* AI SUMMARY */
.ai-panel{background:linear-gradient(135deg,rgba(226,55,68,.08),rgba(255,100,80,.03));
  border:1px solid rgba(226,55,68,.2);border-radius:16px;padding:20px 24px;
  margin-bottom:28px;display:flex;align-items:flex-start;gap:16px;}
.ai-panel-icon{width:44px;height:44px;flex-shrink:0;
  background:linear-gradient(135deg,#E23744,#c0202e);border-radius:12px;
  display:flex;align-items:center;justify-content:center;font-size:22px;
  box-shadow:0 6px 20px rgba(226,55,68,.3);}
.ai-label{font-size:10px;font-weight:800;color:#E23744;text-transform:uppercase;
  letter-spacing:1.8px;margin-bottom:6px;}
.ai-text{font-size:15px;font-weight:400;color:#bbb;line-height:1.65;font-style:italic;}

/* CARDS */
.rcard{background:linear-gradient(145deg,#141414,#111);border:1px solid rgba(255,255,255,.07);
  border-radius:20px;overflow:hidden;position:relative;cursor:pointer;
  transition:transform .35s cubic-bezier(.34,1.56,.64,1),border-color .3s,box-shadow .3s;}
.rcard:hover{transform:translateY(-7px);border-color:rgba(226,55,68,.4);
  box-shadow:0 28px 64px rgba(0,0,0,.55),0 0 0 1px rgba(226,55,68,.22);}
.rcard:hover .cimg{transform:scale(1.08);}
.rank-badge{position:absolute;top:14px;left:14px;z-index:10;display:flex;align-items:center;
  gap:5px;font-size:13px;font-weight:800;padding:5px 12px;border-radius:20px;
  backdrop-filter:blur(10px);}
.gold{background:rgba(255,215,0,.18);border:1px solid rgba(255,215,0,.4);color:#ffd700;}
.silver{background:rgba(192,192,192,.14);border:1px solid rgba(192,192,192,.3);color:#c0c0c0;}
.bronze{background:rgba(205,127,50,.14);border:1px solid rgba(205,127,50,.3);color:#cd7f32;}
.other{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.14);color:#aaa;}
.top-pick-badge{position:absolute;top:14px;right:14px;z-index:10;font-size:10px;font-weight:800;
  color:#fff;background:linear-gradient(135deg,#E23744,#c0202e);border-radius:20px;
  padding:4px 12px;letter-spacing:1px;text-transform:uppercase;
  box-shadow:0 4px 14px rgba(226,55,68,.45);}
.cimg-wrap{position:relative;overflow:hidden;}
.cimg{width:100%;height:100%;object-fit:cover;transition:transform .55s ease;}
.cimg-overlay{position:absolute;bottom:0;left:0;right:0;height:55%;
  background:linear-gradient(to top,rgba(10,10,10,.9),transparent);}
.cbody{padding:22px 24px 24px;}
.cbody-lg{padding:26px 30px 30px;}
.cname{font-size:22px;font-weight:800;color:#fff;margin-bottom:10px;line-height:1.2;}
.cname-sm{font-size:18px;font-weight:700;color:#fff;margin-bottom:8px;line-height:1.2;}
.cmeta{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:14px;}
.crating{display:inline-flex;align-items:center;gap:4px;background:rgba(255,193,7,.1);
  border:1px solid rgba(255,193,7,.25);border-radius:20px;padding:4px 10px;
  font-size:13px;font-weight:700;color:#ffc107;}
.cloc{font-size:13px;color:#777;}
.ccost{font-size:13px;color:#666;}
.ctags{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;}
.ctag{font-size:11px;font-weight:600;color:#888;background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.09);border-radius:6px;padding:3px 10px;}
.cwhy{background:rgba(226,55,68,.06);border-left:3px solid #E23744;
  border-radius:0 8px 8px 0;padding:10px 14px;margin-top:14px;}
.cwhy-lbl{font-size:10px;font-weight:800;color:#E23744;text-transform:uppercase;
  letter-spacing:1.5px;margin-bottom:4px;}
.cwhy-txt{font-size:13px;color:#aaa;font-style:italic;line-height:1.5;}
.cwhy-txt-sm{font-size:12px;color:#aaa;font-style:italic;line-height:1.5;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}
.hero-grid{display:grid;grid-template-columns:1fr 1fr;}
@media(max-width:768px){.hero-grid{grid-template-columns:1fr;}}

/* HOW IT WORKS */
.how-box{margin:48px 0 32px;padding:36px;background:linear-gradient(145deg,#111,#0e0e0e);
  border:1px solid rgba(255,255,255,.06);border-radius:22px;}
.how-ttl{font-size:17px;font-weight:800;color:#fff;margin-bottom:26px;text-align:center;}
.how-steps{display:flex;gap:16px;flex-wrap:wrap;}
.how-step{flex:1;min-width:130px;text-align:center;padding:20px 14px;
  background:rgba(255,255,255,.025);border-radius:14px;border:1px solid rgba(255,255,255,.05);}
.how-num{width:40px;height:40px;background:linear-gradient(135deg,#E23744,#c0202e);
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:16px;font-weight:900;color:#fff;margin:0 auto 12px;
  box-shadow:0 6px 20px rgba(226,55,68,.3);}
.how-txt{font-size:13px;color:#666;line-height:1.55;font-weight:500;}

/* EMPTY STATE */
.empty{text-align:center;padding:80px 40px;background:#111;
  border:1px solid rgba(255,255,255,.07);border-radius:20px;}
.empty-icon{font-size:64px;margin-bottom:20px;}
.empty-ttl{font-size:24px;font-weight:800;color:#fff;margin-bottom:10px;}
.empty-txt{font-size:15px;color:#555;max-width:380px;margin:0 auto;}

/* FOOTER */
.zfooter{background:#0a0a0a;border-top:1px solid rgba(255,255,255,.06);
  padding:48px 40px 32px;margin-top:64px;}
.fbrand{font-size:24px;font-weight:900;color:#fff;margin-bottom:5px;}
.fbrand em{color:#E23744;font-style:normal;}
.ftagline{font-size:13px;color:#444;margin-bottom:30px;}
.fbottom{display:flex;justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:14px;padding-top:24px;border-top:1px solid rgba(255,255,255,.05);}
.fcopy{font-size:12px;color:#333;}
.flinks{display:flex;gap:22px;}
.flinks a{font-size:12px;color:#444;text-decoration:none;transition:color .2s;}
.flinks a:hover{color:#E23744;}

@keyframes fadeInUp{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}
.fade-up{animation:fadeInUp .55s ease forwards;}
.d1{animation-delay:.05s;opacity:0;}
.d2{animation-delay:.15s;opacity:0;}
.d3{animation-delay:.25s;opacity:0;}
</style>
"""

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def rank_badge(rank):
    icons={1:"🥇",2:"🥈",3:"🥉"}
    cls={1:"gold",2:"silver",3:"bronze"}
    return f'<div class="rank-badge {cls.get(rank,"other")}">{icons.get(rank,"")} #{rank}</div>'

def hero_card(rec, rank):
    r = rec.restaurant
    img = get_restaurant_image(r.cuisines, r.name)
    tags = "".join(f'<span class="ctag">🍽 {c}</span>' for c in r.cuisines[:4])
    why = rec.explanation.strip('"')
    return f"""
    <div class="rcard fade-up" style="margin-bottom:20px;">
      <div class="hero-grid">
        <div class="cimg-wrap" style="height:400px;">
          {rank_badge(rank)}
          <div class="top-pick-badge">⚡ Top Pick</div>
          <img class="cimg" src="{img}" alt="{r.name}" loading="lazy"/>
          <div class="cimg-overlay"></div>
        </div>
        <div class="cbody-lg" style="display:flex;flex-direction:column;justify-content:center;background:linear-gradient(145deg,#141414,#111);">
          <div class="cname">{r.name}</div>
          <div class="cmeta">
            <span class="crating">⭐ {r.rating:.1f}</span>
            <span class="cloc">📍 {r.location}</span>
            <span class="ccost">₹{r.estimated_cost:.0f} for two · {r.budget_band.capitalize()}</span>
          </div>
          <div class="ctags">{tags}</div>
          <div class="cwhy">
            <div class="cwhy-lbl">✦ Why Zomato AI Picked This</div>
            <div class="cwhy-txt">"{why}"</div>
          </div>
        </div>
      </div>
    </div>"""

def small_card(rec, rank, delay=0):
    r = rec.restaurant
    img = get_restaurant_image(r.cuisines, r.name)
    tags = "".join(f'<span class="ctag">🍽 {c}</span>' for c in r.cuisines[:3])
    why = rec.explanation.strip('"')
    dc = f"d{delay}" if delay else ""
    return f"""
    <div class="rcard fade-up {dc}">
      <div class="cimg-wrap" style="height:210px;">
        {rank_badge(rank)}
        <img class="cimg" src="{img}" alt="{r.name}" loading="lazy"/>
        <div class="cimg-overlay"></div>
      </div>
      <div class="cbody">
        <div class="cname-sm">{r.name}</div>
        <div class="cmeta">
          <span class="crating">⭐ {r.rating:.1f}</span>
          <span class="cloc">📍 {r.location}</span>
        </div>
        <div class="ctags">{tags}</div>
        <div style="font-size:12px;color:#555;margin-bottom:10px;">₹{r.estimated_cost:.0f} for two</div>
        <div class="cwhy">
          <div class="cwhy-lbl">✦ Why Picked</div>
          <div class="cwhy-txt-sm">"{why}"</div>
        </div>
      </div>
    </div>"""

def main():
    st.markdown(CSS, unsafe_allow_html=True)

    # NAV
    st.markdown("""
    <div class="page-top">
    <nav class="zomato-nav">
      <div style="display:flex;align-items:center;">
        <div class="nav-logo">🍽️</div>
        <span class="nav-name">Zomato<em> AI</em></span>
        <span class="nav-beta">Beta</span>
      </div>
      <div style="display:flex;align-items:center;">
        <div class="nav-city">📍 Bangalore</div>
        <div class="nav-avatar">U</div>
      </div>
    </nav>
    <div style="background: rgba(226, 55, 68, 0.12); border: 1px solid rgba(226, 55, 68, 0.3); padding: 12px 24px; border-radius: 12px; margin: 20px 40px 0; text-align: center; font-family: 'Inter', sans-serif;">
      ✨ <strong>Try our new Premium Web App!</strong> Experience smooth glassmorphism, responsive sliders, and micro-animations at <a href="http://localhost:8000" target="_blank" style="color: #ff8f96; text-decoration: underline; font-weight: 700;">http://localhost:8000</a>.
    </div>
    """, unsafe_allow_html=True)

    # HERO
    st.markdown("""
    <section class="hero">
      <div class="hero-glow"></div>
      <div class="hero-pill">✨ AI-Powered Restaurant Discovery</div>
      <h1 class="hero-h1">Find Your Perfect<br><span class="red">Dining Experience</span></h1>
      <p class="hero-sub">Zomato AI understands your taste, budget &amp; mood to recommend the ideal restaurant — powered by real data and Llama&nbsp;3.</p>
      <div class="hero-stats">
        <div><div class="stat-num">10K+</div><div class="stat-lbl">Restaurants</div></div>
        <div class="stat-divider"></div>
        <div><div class="stat-num">50+</div><div class="stat-lbl">Cuisines</div></div>
        <div class="stat-divider"></div>
        <div><div class="stat-num">AI</div><div class="stat-lbl">Powered</div></div>
        <div class="stat-divider"></div>
        <div><div class="stat-num">Free</div><div class="stat-lbl">Always</div></div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    # HEALTH CHECK
    backend_healthy = False
    try:
        hr = requests.get(f"{BACKEND_URL}/api/v1/health", timeout=3)
        if hr.status_code == 200 and hr.json().get("status") == "healthy":
            backend_healthy = True
    except Exception:
        pass

    # MAIN CONTENT
    st.markdown('<div class="wrap">', unsafe_allow_html=True)

    if not backend_healthy:
        st.markdown("""
        <div class="bar-err">
          ⚠️ <div><strong>Backend offline</strong> — Cannot reach 
          <code style="background:rgba(226,55,68,.15);padding:2px 6px;border-radius:4px;font-size:12px;">http://localhost:8000</code>.
          Start the backend server first.</div>
        </div>""", unsafe_allow_html=True)

    # FETCH METADATA
    locations, cuisines = [], []
    if backend_healthy:
        try:
            lr = requests.get(f"{BACKEND_URL}/api/v1/metadata/locations", timeout=5)
            if lr.status_code == 200: locations = lr.json()
        except Exception: pass
        try:
            cr = requests.get(f"{BACKEND_URL}/api/v1/metadata/cuisines", timeout=5)
            if cr.status_code == 200: cuisines = cr.json()
        except Exception: pass

    if not locations:
        locations = ["Banashankari","Jayanagar","JP Nagar","Indiranagar","Koramangala",
                     "Whitefield","HSR Layout","BTM Layout","Marathahalli","Electronic City"]
    if not cuisines:
        cuisines = ["North Indian","South Indian","Chinese","Continental","Italian",
                    "Mughlai","Biryani","Street Food","Cafe","Desserts"]

    # PREFS CARD
    st.markdown("""
    <div class="prefs-card">
      <div class="prefs-title">
        <div class="prefs-icon">⚙️</div> Customize Your Preferences
      </div>
      <div class="prefs-sub">Tell us what you're craving and our AI handles the rest</div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([2,2,2,2])
    with c1: location = st.selectbox("📍 Location", options=locations)
    with c2: cuisine = st.selectbox("🍽 Cuisine", options=cuisines)
    with c3: budget = st.radio("💰 Budget", ["Low","Medium","High"], index=1, horizontal=True)
    with c4: min_rating = st.slider("⭐ Min Rating", 0.0, 5.0, 4.0, 0.1)

    additional = st.text_input("🎯 Vibe / Special Notes",
        placeholder="e.g., rooftop dining, family friendly, quick lunch, live music...")

    cc1, cc2, cc3 = st.columns([3,2,3])
    with cc2: top_k = st.slider("🔢 Number of picks", 1, 5, 3)

    st.markdown("</div>", unsafe_allow_html=True)

    # CTA
    b1, b2, b3 = st.columns([2,2,2])
    with b2:
        clicked = st.button("🔍  Find My Perfect Restaurant",
                            disabled=not backend_healthy, use_container_width=True)

    # RESULTS
    if clicked and backend_healthy:
        prefs = UserPreferences(location=location, budget=budget.lower(),
                                cuisine=cuisine, min_rating=min_rating,
                                additional_preferences=additional, top_k=top_k)
        response = None
        with st.spinner("🤖 Zomato AI is curating your perfect picks..."):
            try:
                resp = requests.post(f"{BACKEND_URL}/api/v1/recommendations",
                                     json=prefs.model_dump(), timeout=30)
                if resp.status_code == 200:
                    response = RecommendationResponse.model_validate(resp.json())
                else:
                    st.markdown(f'<div class="bar-err">❌ API Error ({resp.status_code}): {resp.text}</div>',
                                unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="bar-err">❌ Connection Error: {e}</div>',
                            unsafe_allow_html=True)

        if response:
            if not response.recommendations:
                st.markdown("""
                <div class="empty">
                  <div class="empty-icon">🔍</div>
                  <div class="empty-ttl">No restaurants matched</div>
                  <div class="empty-txt">Try adjusting your filters — location, cuisine, or minimum rating.</div>
                </div>""", unsafe_allow_html=True)
            else:
                recs = response.recommendations
                n = len(recs)
                st.markdown(f"""
                <div class="results-hdr">
                  <div class="results-ttl">🍽️ Your Curated Picks</div>
                  <div class="results-badge">{n} result{"s" if n!=1 else ""} found</div>
                </div>""", unsafe_allow_html=True)

                if response.summary:
                    summary = response.summary.strip('"')
                    st.markdown(f"""
                    <div class="ai-panel">
                      <div class="ai-panel-icon">✨</div>
                      <div>
                        <div class="ai-label">AI Insight</div>
                        <div class="ai-text">"{summary}"</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

                if n == 1:
                    st.markdown(hero_card(recs[0], 1), unsafe_allow_html=True)
                elif n == 2:
                    ca, cb = st.columns(2)
                    with ca: st.markdown(small_card(recs[0], 1, 1), unsafe_allow_html=True)
                    with cb: st.markdown(small_card(recs[1], 2, 2), unsafe_allow_html=True)
                else:
                    st.markdown(hero_card(recs[0], 1), unsafe_allow_html=True)
                    remaining = recs[1:]
                    cols = st.columns(min(len(remaining), 2))
                    for i, rec in enumerate(remaining):
                        with cols[i % 2]:
                            st.markdown(small_card(rec, i+2, min(i+1,3)), unsafe_allow_html=True)
    elif not backend_healthy:
        st.markdown("""
        <div class="bar-info">💡 Start the backend server to unlock AI-powered recommendations.</div>
        <div class="how-box">
          <div class="how-ttl">✦ How Zomato AI Works</div>
          <div class="how-steps">
            <div class="how-step"><div class="how-num">1</div><div class="how-txt">Set location, cuisine &amp; budget preferences</div></div>
            <div class="how-step"><div class="how-num">2</div><div class="how-txt">AI filters thousands of Bangalore restaurants</div></div>
            <div class="how-step"><div class="how-num">3</div><div class="how-txt">Llama 3 ranks &amp; explains each recommendation</div></div>
            <div class="how-step"><div class="how-num">4</div><div class="how-txt">Discover your next favourite spot instantly</div></div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="bar-ok">✅ Backend connected! Set your preferences above and click <strong>Find My Perfect Restaurant</strong>.</div>
        <div class="how-box">
          <div class="how-ttl">✦ How Zomato AI Works</div>
          <div class="how-steps">
            <div class="how-step"><div class="how-num">1</div><div class="how-txt">Set location, cuisine &amp; budget preferences</div></div>
            <div class="how-step"><div class="how-num">2</div><div class="how-txt">AI filters thousands of Bangalore restaurants</div></div>
            <div class="how-step"><div class="how-num">3</div><div class="how-txt">Llama 3 ranks &amp; explains each recommendation</div></div>
            <div class="how-step"><div class="how-num">4</div><div class="how-txt">Discover your next favourite spot instantly</div></div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close wrap

    # FOOTER
    st.markdown("""
    <div class="zfooter">
      <div class="fbrand">Zomato<em> AI</em></div>
      <div class="ftagline">AI-powered culinary intelligence for Bangalore</div>
      <div class="fbottom">
        <div class="fcopy">© 2025 Zomato AI · Powered by Llama 3 · Real restaurant data</div>
        <div class="flinks">
          <a href="#">Terms</a><a href="#">Privacy</a><a href="#">API Docs</a><a href="#">Support</a>
        </div>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
