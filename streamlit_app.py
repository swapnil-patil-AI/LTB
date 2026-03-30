"""
LTB Analytics Demo — Look-to-Book Intelligence Platform
Management Demo Application
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random
import datetime
import json
import urllib.request

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LTB Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Auth ─────────────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "login_error" not in st.session_state:
    st.session_state["login_error"] = False

INFOSYS_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 50" width="140" height="40">
  <!-- Infosys wordmark — simplified geometric recreation -->
  <rect width="180" height="50" fill="transparent"/>
  <!-- "i" dot -->
  <circle cx="8" cy="10" r="4.5" fill="#007CC3"/>
  <!-- "i" stem + n + f + o + s + y + s letters as simple bold shapes -->
  <!-- Using text as fallback since full SVG path recreation is complex -->
  <text x="4" y="42" font-family="Arial Black,Arial,sans-serif" font-size="28"
        font-weight="900" fill="#007CC3" letter-spacing="-1">infosys</text>
</svg>
"""

INFOSYS_FULL_HTML = """
<div style="display:flex;align-items:center;gap:10px;">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 52" width="110" height="28">
    <rect width="200" height="52" fill="transparent"/>
    <text x="2" y="42" font-family="Arial Black,Arial,sans-serif" font-size="34"
          font-weight="900" fill="#007CC3" letter-spacing="-1.5">infosys</text>
  </svg>
  <div style="border-left:2px solid #CBD5E1;padding-left:10px;line-height:1.25;">
    <div style="font-size:.62rem;color:#64748B;text-transform:uppercase;letter-spacing:1.2px;font-weight:600;">An</div>
    <div style="font-size:.8rem;font-weight:800;color:#0D1B2A;letter-spacing:.3px;">Travel &amp; Hospitality</div>
    <div style="font-size:.62rem;color:#64748B;text-transform:uppercase;letter-spacing:1.2px;font-weight:600;">Initiative</div>
  </div>
</div>
"""

INFOSYS_SIDEBAR_HTML = """
<div style="text-align:center;padding:10px 0 4px;">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 52" width="100" height="26">
    <text x="2" y="42" font-family="Arial Black,Arial,sans-serif" font-size="34"
          font-weight="900" fill="#64B5F6" letter-spacing="-1.5">infosys</text>
  </svg>
  <div style="font-size:.68rem;color:#90CAF9;margin-top:2px;letter-spacing:.8px;">
    Travel &amp; Hospitality Initiative
  </div>
</div>
"""

def show_login():
    """Render login page."""
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg,#0D1B2A 0%,#1A2E45 50%,#0D3B6E 100%) !important; }
    [data-testid="stSidebar"] { display: none; }
    header { display: none; }
    .login-card {
        background: rgba(255,255,255,0.96);
        border-radius: 20px;
        padding: 44px 40px 36px;
        box-shadow: 0 24px 80px rgba(0,0,0,0.35);
        max-width: 440px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

    # Centre vertically
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        st.markdown("""
        <div class="login-card">

          <!-- Infosys brand -->
          <div style="text-align:center;margin-bottom:6px;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 52" width="130" height="34">
              <text x="2" y="42" font-family="Arial Black,Arial,sans-serif" font-size="34"
                    font-weight="900" fill="#007CC3" letter-spacing="-1.5">infosys</text>
            </svg>
          </div>
          <div style="text-align:center;font-size:.72rem;color:#64748B;letter-spacing:1.2px;
                      text-transform:uppercase;font-weight:600;margin-bottom:24px;">
            Travel &amp; Hospitality Initiative
          </div>

          <!-- Product logo -->
          <div style="text-align:center;margin-bottom:8px;">
            <div style="display:inline-flex;align-items:center;justify-content:center;
                        width:62px;height:62px;border-radius:50%;
                        background:linear-gradient(145deg,#1565C0,#0D1B2A);
                        box-shadow:0 8px 24px rgba(21,101,192,0.35);margin-bottom:12px;">
              <span style="font-size:26px;">📊</span>
            </div>
          </div>
          <div style="text-align:center;font-size:1.45rem;font-weight:900;color:#0D1B2A;
                      letter-spacing:.3px;margin-bottom:4px;">LTB Analytics Platform</div>
          <div style="text-align:center;font-size:.82rem;color:#64748B;margin-bottom:28px;">
            Look-to-Book Intelligence · Air Canada NDC
          </div>
          <hr style="border:none;border-top:1px solid #E2E8F0;margin-bottom:24px;">
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
            if st.session_state["login_error"]:
                st.markdown('<div style="color:#C62828;font-size:.82rem;text-align:center;margin-top:-8px;">❌ Invalid credentials. Please try again.</div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")
            if submitted:
                if username == "Admin" and password == "Admin@123":
                    st.session_state["authenticated"] = True
                    st.session_state["login_error"]   = False
                    st.rerun()
                else:
                    st.session_state["login_error"] = True
                    st.rerun()

        st.markdown("""
        <div style="text-align:center;margin-top:16px;font-size:.75rem;color:rgba(255,255,255,0.45);">
          Demo credentials: <strong style="color:rgba(255,255,255,0.65);">Admin</strong> /
          <strong style="color:rgba(255,255,255,0.65);">Admin@123</strong>
        </div>
        """, unsafe_allow_html=True)


# ── Gate: show login if not authenticated ─────────────────────────────────────
if not st.session_state["authenticated"]:
    show_login()
    st.stop()

# ── Colour tokens ─────────────────────────────────────────────────────────────
NAVY   = "#0D1B2A"
BLUE   = "#1565C0"
TEAL   = "#00695C"
GREEN  = "#2E7D32"
AMBER  = "#E65100"
RED    = "#C62828"
PURPLE = "#4527A0"
GOLD   = "#F9A825"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Base */
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
.stApp { background: #F0F4F8; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0D1B2A 0%, #1A2E45 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: #E0E8F0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: #90CAF9 !important; }

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    border: 1px solid #E0E8F0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 12px;
}
.metric-num { font-size: 2.2rem; font-weight: 800; line-height: 1.1; }
.metric-label { font-size: 0.8rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }
.metric-sub { font-size: 0.78rem; color: #94A3B8; margin-top: 4px; }

/* Status badges */
.badge-low    { background:#E8F5E9; color:#2E7D32; padding:3px 10px; border-radius:12px; font-size:.75rem; font-weight:700; }
.badge-medium { background:#FFF3E0; color:#E65100; padding:3px 10px; border-radius:12px; font-size:.75rem; font-weight:700; }
.badge-high   { background:#FFEBEE; color:#C62828; padding:3px 10px; border-radius:12px; font-size:.75rem; font-weight:700; }
.badge-na     { background:#F5F5F5; color:#9E9E9E; padding:3px 10px; border-radius:12px; font-size:.75rem; font-weight:700; }

/* Page header */
.page-header {
    background: linear-gradient(135deg, #0D1B2A 0%, #1565C0 100%);
    border-radius: 14px;
    padding: 20px 28px 14px;
    margin-bottom: 24px;
    color: white;
}
.page-header h2 { margin: 0; font-size: 1.55rem; font-weight: 800; }
.page-header p  { margin: 4px 0 0; opacity: 0.75; font-size: .88rem; }
.page-header .infosys-bar {
    display: flex; align-items: center; justify-content: flex-end;
    margin-top: 12px; padding-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.15);
    gap: 8px;
}
.page-header .infosys-bar svg text { fill: rgba(255,255,255,0.85) !important; }
.page-header .infosys-bar .inf-label {
    font-size:.65rem; color:rgba(255,255,255,0.6); text-transform:uppercase;
    letter-spacing:1.2px; font-weight:600; line-height:1.3;
}

/* Callout boxes */
.callout-info   { background:#EFF6FF; border-left:4px solid #1565C0; border-radius:8px; padding:14px 16px; margin:12px 0; }
.callout-success{ background:#E8F5E9; border-left:4px solid #2E7D32; border-radius:8px; padding:14px 16px; margin:12px 0; }
.callout-warn   { background:#FFF3E0; border-left:4px solid #E65100; border-radius:8px; padding:14px 16px; margin:12px 0; }
.callout-danger { background:#FFEBEE; border-left:4px solid #C62828; border-radius:8px; padding:14px 16px; margin:12px 0; }

/* Route row */
.route-row {
    background: white; border-radius: 10px; padding: 14px 18px;
    margin: 6px 0; border: 1px solid #E8EEF4;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}

/* Rule card */
.rule-card {
    background: white; border-radius: 12px; padding: 16px 20px;
    margin: 8px 0; border: 1px solid #E0E8F0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* AI Chat */
.ai-bubble {
    background: linear-gradient(135deg,#1565C0,#0D47A1);
    border-radius: 14px 14px 14px 4px;
    padding: 14px 18px; color: white; margin: 8px 0;
    font-size: .9rem; line-height: 1.6;
}
.user-bubble {
    background: #E3F2FD; border-radius: 14px 14px 4px 14px;
    padding: 12px 16px; color: #1A237E; margin: 8px 0 8px auto;
    font-size: .9rem; line-height: 1.6; max-width: 85%;
}

/* Tab override */
[data-testid="stHorizontalBlock"] { gap: 12px; }

/* Divider */
.section-divider {
    border: none; border-top: 1px solid #E0E8F0; margin: 20px 0;
}

/* Animated badge */
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }
.live-badge {
    display:inline-block; background:#E8F5E9; color:#2E7D32;
    border-radius:12px; padding:2px 10px; font-size:.72rem;
    font-weight:700; animation: pulse 2.5s infinite;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DUMMY DATA GENERATION
# ══════════════════════════════════════════════════════════════════════════════

SELLERS = {
    "Sabre (ac.gndc.sabre)":          {"code":"sabre",       "color":BLUE,   "tier":"Premium"},
    "Travelport (ac.gndc.travelport)": {"code":"travelport",  "color":TEAL,   "tier":"Standard"},
    "Amadeus (ac.gndc.amadeus)":       {"code":"amadeus",     "color":PURPLE, "tier":"Premium"},
    "FareNexus (ac.gndc.farenexus)":   {"code":"farenexus",   "color":AMBER,  "tier":"Standard"},
    "NDCConnect (ac.gndc.ndcconnect)": {"code":"ndcconnect",  "color":GREEN,  "tier":"Trial"},
}

ROUTES = [
    "YUL→LHR","YYZ→CDG","YVR→NRT","YYC→LAX","YUL→DXB",
    "YYZ→FRA","YVR→ICN","YUL→GRU","YYZ→MIA","YOW→LHR",
    "YHZ→LHR","YEG→LAX","YYZ→SYD","YUL→ZRH","YYZ→DEL",
]

@st.cache_data
def generate_data():
    """Generate 30 days of realistic LTB data per seller per route."""
    random.seed(42)
    today = datetime.date.today()
    records = []

    # Each seller has a base LTB profile per route
    seller_profiles = {
        "sabre":       {"base_ltb":8,  "variance":6,  "order_base":25},
        "travelport":  {"base_ltb":22, "variance":12, "order_base":12},
        "amadeus":     {"base_ltb":5,  "variance":3,  "order_base":40},
        "farenexus":   {"base_ltb":35, "variance":18, "order_base":8},
        "ndcconnect":  {"base_ltb":48, "variance":22, "order_base":4},
    }

    route_multipliers = {
        "YUL→LHR":1.2,"YYZ→CDG":1.0,"YVR→NRT":1.4,"YYC→LAX":0.8,"YUL→DXB":1.6,
        "YYZ→FRA":1.1,"YVR→ICN":1.3,"YUL→GRU":0.9,"YYZ→MIA":0.7,"YOW→LHR":1.5,
        "YHZ→LHR":1.8,"YEG→LAX":0.6,"YYZ→SYD":1.9,"YUL→ZRH":1.0,"YYZ→DEL":1.7,
    }

    for seller_name, seller_info in SELLERS.items():
        code = seller_info["code"]
        profile = seller_profiles[code]

        for route in ROUTES:
            mult = route_multipliers[route]
            for days_ago in range(30, 0, -1):
                date = today - datetime.timedelta(days=days_ago)
                # Add day-of-week and trend effects
                dow_factor = 1.3 if date.weekday() < 5 else 0.6
                trend = 1 + (random.uniform(-0.05, 0.05) * days_ago / 30)

                order_count = max(1, int(profile["order_base"] * mult * dow_factor * trend + random.randint(-3, 3)))
                ltb = max(1.0, profile["base_ltb"] * mult + random.uniform(-profile["variance"], profile["variance"]))
                shopping_count = int(ltb * order_count)

                records.append({
                    "date":           date,
                    "seller_name":    seller_name,
                    "seller_code":    code,
                    "route":          route,
                    "shopping_count": shopping_count,
                    "order_count":    order_count,
                    "daily_ltb":      round(ltb, 2),
                })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    return df


def compute_rolling(df, window_days):
    """Compute rolling LTB for given window."""
    cutoff = pd.Timestamp(datetime.date.today() - datetime.timedelta(days=window_days))
    grp = df[df["date"] >= cutoff].groupby(["seller_name","route"]).agg(
        shopping_total=("shopping_count","sum"),
        order_total=("order_count","sum")
    ).reset_index()
    grp[f"ltb_{window_days}d"] = (grp["shopping_total"] / grp["order_total"]).round(2)
    return grp[["seller_name","route",f"ltb_{window_days}d","shopping_total","order_total"]]


def get_ltb_status(ltb):
    if ltb is None or pd.isna(ltb): return "N/A",  "badge-na",   "⚪"
    if ltb < 8:  return "Excellent", "badge-low",    "🟢"
    if ltb < 20: return "Good",      "badge-low",    "🟢"
    if ltb < 30: return "Warning",   "badge-medium", "🟡"
    if ltb < 50: return "High",      "badge-high",   "🔴"
    return "Critical", "badge-high", "🔴"


def get_routing_decision(ltb, rules):
    """Evaluate rules in priority order."""
    for rule in sorted(rules, key=lambda r: r["priority"]):
        if not rule.get("enabled", True):
            continue
        s_match = rule["seller"] == "*" or rule["seller"] in ["All Sellers"]
        ltb_ok = False
        op, thresh = rule["operator"], rule["threshold"]
        if   op == ">":  ltb_ok = ltb >  thresh
        elif op == ">=": ltb_ok = ltb >= thresh
        elif op == "<":  ltb_ok = ltb <  thresh
        elif op == "<=": ltb_ok = ltb <= thresh
        if s_match and ltb_ok:
            return rule["action"], rule["name"]
    return "Normal Search", "Default"


# ── Load data ─────────────────────────────────────────────────────────────────
df = generate_data()
today_df  = df[df["date"] == df["date"].max()].copy()
roll7  = compute_rolling(df, 7)
roll14 = compute_rolling(df, 14)
roll30 = compute_rolling(df, 30)

# Merge rolling windows
summary = today_df.groupby(["seller_name","route","seller_code"]).agg(
    daily_ltb=("daily_ltb","mean"),
    shopping_count=("shopping_count","sum"),
    order_count=("order_count","sum"),
).reset_index()
summary = summary.merge(roll7[["seller_name","route","ltb_7d"]], on=["seller_name","route"], how="left")
summary = summary.merge(roll14[["seller_name","route","ltb_14d"]], on=["seller_name","route"], how="left")
summary = summary.merge(roll30[["seller_name","route","ltb_30d"]], on=["seller_name","route"], how="left")


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════

if "rules" not in st.session_state:
    st.session_state["rules"] = [
        {"id":1,"priority":1,"name":"Sabre DUB→LHR High LTB","seller":"All Sellers","operator":">","threshold":40,"window":"Daily","action":"Massive Search","enabled":True},
        {"id":2,"priority":2,"name":"Any Seller Very High LTB","seller":"All Sellers","operator":">","threshold":30,"window":"7-Day Rolling","action":"Massive Search","enabled":True},
        {"id":3,"priority":3,"name":"Travelport High LTB","seller":"Travelport (ac.gndc.travelport)","operator":">","threshold":20,"window":"7-Day Rolling","action":"Massive Search","enabled":True},
        {"id":4,"priority":4,"name":"Amadeus Low LTB","seller":"Amadeus (ac.gndc.amadeus)","operator":"<","threshold":8,"window":"Daily","action":"Normal Search","enabled":True},
        {"id":5,"priority":99,"name":"Default Fallback","seller":"All Sellers","operator":">=","threshold":0,"window":"Daily","action":"Normal Search","enabled":True},
    ]

if "ai_messages" not in st.session_state:
    st.session_state["ai_messages"] = []

if "chat_input_key" not in st.session_state:
    st.session_state["chat_input_key"] = 0


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Infosys branding at top of sidebar
    st.markdown(INFOSYS_SIDEBAR_HTML, unsafe_allow_html=True)
    st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.12);margin:4px 0 12px;">', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:8px 0 14px;">
      <div style="display:inline-flex;align-items:center;justify-content:center;
                  width:52px;height:52px;border-radius:50%;
                  background:linear-gradient(145deg,#1565C0,#0D1B2A);
                  box-shadow:0 6px 20px rgba(21,101,192,0.4);margin-bottom:10px;">
        <span style="font-size:22px;">📊</span>
      </div>
      <div style="font-size:1.05rem;font-weight:800;letter-spacing:.5px;">LTB Analytics</div>
      <div style="font-size:.7rem;opacity:.6;margin-top:2px;">Look-to-Book Intelligence Platform</div>
      <div style="margin-top:8px;"><span class="live-badge">● LIVE DEMO</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**🗓 Data Date**")
    data_date = st.date_input("", value=datetime.date.today(), label_visibility="collapsed")

    st.markdown("**👤 Seller Filter**")
    all_sellers = ["All Sellers"] + list(SELLERS.keys())
    selected_seller = st.selectbox("", all_sellers, label_visibility="collapsed")

    st.markdown("**✈️ Route Filter**")
    selected_route = st.selectbox("", ["All Routes"] + ROUTES, label_visibility="collapsed")

    st.markdown("**📅 LTB Window**")
    window_choice = st.selectbox("", ["Daily", "7-Day Rolling", "14-Day Rolling", "30-Day Rolling"], label_visibility="collapsed")
    window_map = {"Daily":"daily_ltb","7-Day Rolling":"ltb_7d","14-Day Rolling":"ltb_14d","30-Day Rolling":"ltb_30d"}
    active_col = window_map[window_choice]

    st.markdown("---")
    # Quick stats
    total_sellers = len(SELLERS)
    total_routes  = len(ROUTES)
    high_ltb = summary[summary["daily_ltb"] >= 30].shape[0]
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.06);border-radius:10px;padding:14px 16px;">
      <div style="font-size:.72rem;opacity:.6;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Quick Stats</div>
      <div style="display:flex;justify-content:space-between;margin:6px 0;">
        <span style="opacity:.75;font-size:.82rem;">Sellers tracked</span>
        <span style="font-weight:700;color:#90CAF9;">{total_sellers}</span>
      </div>
      <div style="display:flex;justify-content:space-between;margin:6px 0;">
        <span style="opacity:.75;font-size:.82rem;">Routes monitored</span>
        <span style="font-weight:700;color:#90CAF9;">{total_routes}</span>
      </div>
      <div style="display:flex;justify-content:space-between;margin:6px 0;">
        <span style="opacity:.75;font-size:.82rem;">High LTB routes</span>
        <span style="font-weight:700;color:#EF9A9A;">{high_ltb}</span>
      </div>
      <div style="display:flex;justify-content:space-between;margin:6px 0;">
        <span style="opacity:.75;font-size:.82rem;">Active rules</span>
        <span style="font-weight:700;color:#A5D6A7;">{sum(1 for r in st.session_state['rules'] if r['enabled'])}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    try:
        ak = st.secrets.get("ANTHROPIC_API_KEY","")
    except:
        ak = ""
    if not ak:
        ak = st.text_input("🤖 Anthropic API Key", type="password", placeholder="sk-ant-...", key="sidebar_ak")
        if ak:
            st.session_state["anthropic_api_key"] = ak
    else:
        st.session_state["anthropic_api_key"] = ak
        st.markdown('<div style="color:#A5D6A7;font-size:.78rem;">✅ AI key configured</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🚪 Sign Out", use_container_width=True, key="logout_btn"):
        st.session_state["authenticated"] = False
        st.session_state["login_error"]   = False
        st.rerun()
    st.markdown('<div style="font-size:.7rem;opacity:.45;text-align:center;margin-top:4px;">Signed in as Admin</div>', unsafe_allow_html=True)


# ── Filter data based on sidebar ──────────────────────────────────────────────
view_df = summary.copy()
if selected_seller != "All Sellers":
    view_df = view_df[view_df["seller_name"] == selected_seller]
if selected_route != "All Routes":
    view_df = view_df[view_df["route"] == selected_route]


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════

tabs = st.tabs(["🏠 Dashboard", "📊 LTB Analytics", "📈 Charts & Trends", "⚖️ Rule Engine", "🤖 AI Insights"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""
    <div class="page-header">
      <h2>📊 Executive Dashboard</h2>
      <p>Real-time Look-to-Book intelligence across all sellers and routes</p>
      <div class="infosys-bar">
        <div class="inf-label">An</div>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 52" width="82" height="21">
          <text x="2" y="42" font-family="Arial Black,Arial,sans-serif" font-size="34"
                font-weight="900" fill="rgba(255,255,255,0.85)" letter-spacing="-1.5">infosys</text>
        </svg>
        <div class="inf-label">Travel &amp; Hospitality<br>Initiative</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    avg_daily  = summary["daily_ltb"].mean()
    avg_7d     = summary["ltb_7d"].mean()
    critical   = summary[summary["daily_ltb"] >= 50].shape[0]
    excellent  = summary[summary["daily_ltb"] < 10].shape[0]
    ms_routes  = summary[summary["daily_ltb"] >= 30].shape[0]
    total_searches = summary["shopping_count"].sum()
    total_orders   = summary["order_count"].sum()

    c1,c2,c3,c4,c5 = st.columns(5)
    for col, num, lbl, sub, color in [
        (c1, f"{avg_daily:.1f}:1", "Avg Daily LTB", "Platform average today", BLUE),
        (c2, f"{avg_7d:.1f}:1",   "Avg 7-Day LTB", "Rolling window average", TEAL),
        (c3, str(ms_routes),       "Routes → Massive Search", "LTB ≥ 30 threshold", RED),
        (c4, str(excellent),       "Excellent Routes", "LTB < 10 (high converting)", GREEN),
        (c5, f"{total_searches:,}","Total Searches Today", f"{total_orders:,} bookings", AMBER),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-top:3px solid {color};">
              <div class="metric-num" style="color:{color};">{num}</div>
              <div class="metric-label">{lbl}</div>
              <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Seller summary cards
    st.markdown("### 👤 Seller Performance Summary")
    cols = st.columns(len(SELLERS))
    for i, (seller_name, seller_info) in enumerate(SELLERS.items()):
        with cols[i]:
            s_data = summary[summary["seller_name"] == seller_name]
            avg_ltb = s_data["daily_ltb"].mean()
            status, badge_cls, icon = get_ltb_status(avg_ltb)
            high_r  = s_data[s_data["daily_ltb"] >= 30].shape[0]
            top_route = s_data.sort_values("daily_ltb", ascending=False).iloc[0]["route"] if len(s_data) > 0 else "—"
            color = seller_info["color"]
            st.markdown(f"""
            <div class="metric-card" style="border-top:4px solid {color};min-height:170px;">
              <div style="font-size:.72rem;opacity:.55;text-transform:uppercase;letter-spacing:1px;">{seller_info['tier']}</div>
              <div style="font-weight:800;font-size:.92rem;color:{color};margin:4px 0;">{seller_name.split('(')[0].strip()}</div>
              <div style="font-size:1.9rem;font-weight:800;color:{color};">{avg_ltb:.1f}:1</div>
              <div style="margin:6px 0;"><span class="{badge_cls}">{icon} {status}</span></div>
              <div style="font-size:.75rem;color:#64748B;">{high_r} high-LTB routes</div>
              <div style="font-size:.72rem;color:#94A3B8;">Worst: {top_route}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Top 10 worst routes table
    c_left, c_right = st.columns([1.2, 1])
    with c_left:
        st.markdown("### 🚨 Top Routes Needing Attention")
        worst = summary.sort_values("daily_ltb", ascending=False).head(10)
        for _, row in worst.iterrows():
            status, badge_cls, icon = get_ltb_status(row["daily_ltb"])
            routing, rule_name = get_routing_decision(row["daily_ltb"], st.session_state["rules"])
            route_color = RED if row["daily_ltb"] >= 30 else (AMBER if row["daily_ltb"] >= 15 else GREEN)
            seller_short = row["seller_name"].split("(")[0].strip()
            st.markdown(f"""
            <div class="route-row">
              <div>
                <span style="font-weight:700;font-size:.92rem;">{row['route']}</span>
                <span style="font-size:.75rem;color:#94A3B8;margin-left:8px;">{seller_short}</span>
              </div>
              <div style="display:flex;align-items:center;gap:10px;">
                <span style="font-size:1.1rem;font-weight:800;color:{route_color};">{row['daily_ltb']:.1f}</span>
                <span class="{badge_cls}">{status}</span>
                <span style="font-size:.72rem;color:{'#C62828' if 'Massive' in routing else '#2E7D32'};font-weight:700;">→ {routing}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with c_right:
        st.markdown("### 🥧 Routing Distribution")
        massive_count = summary[summary["daily_ltb"] >= 30].shape[0]
        normal_count  = len(summary) - massive_count
        fig_pie = go.Figure(data=[go.Pie(
            labels=["Normal Search (Flex Pricer)", "Massive Search"],
            values=[normal_count, massive_count],
            hole=0.55,
            marker_colors=["#2E7D32", "#C62828"],
            textinfo="label+percent",
            textfont_size=12,
        )])
        fig_pie.update_layout(
            showlegend=False, height=280,
            margin=dict(l=10,r=10,t=10,b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text=f"{len(summary)}<br>routes", x=0.5, y=0.5,
                              font_size=16, font_color="#1A237E", showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # LTB distribution bar
        st.markdown("### 📊 LTB Distribution by Seller")
        seller_avg = summary.groupby("seller_name")["daily_ltb"].mean().sort_values()
        short_names = [n.split("(")[0].strip() for n in seller_avg.index]
        colors_list = [SELLERS[n]["color"] for n in seller_avg.index]
        fig_bar = go.Figure(go.Bar(
            x=seller_avg.values, y=short_names, orientation="h",
            marker_color=colors_list,
            text=[f"{v:.1f}" for v in seller_avg.values],
            textposition="outside",
        ))
        fig_bar.update_layout(
            height=220, margin=dict(l=10,r=40,t=10,b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E8EEF4", title="Avg Daily LTB"),
            yaxis=dict(showgrid=False),
            font_family="Segoe UI",
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LTB ANALYTICS TABLE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("""
    <div class="page-header">
      <h2>📊 LTB Analytics — Detailed View</h2>
      <p>Daily and rolling Look-to-Book ratios per seller per route</p>
      <div class="infosys-bar">
        <div class="inf-label">An</div>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 52" width="82" height="21">
          <text x="2" y="42" font-family="Arial Black,Arial,sans-serif" font-size="34"
                font-weight="900" fill="rgba(255,255,255,0.85)" letter-spacing="-1.5">infosys</text>
        </svg>
        <div class="inf-label">Travel &amp; Hospitality<br>Initiative</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Summary callout
    if selected_seller != "All Sellers":
        s_info = SELLERS[selected_seller]
        s_avg  = view_df["daily_ltb"].mean()
        status, badge_cls, icon = get_ltb_status(s_avg)
        st.markdown(f"""
        <div class="callout-info">
          <strong style="color:{s_info['color']};">{selected_seller}</strong> — 
          Average daily LTB today: <strong style="color:{s_info['color']};">{s_avg:.1f}:1</strong>
          &nbsp;<span class="{badge_cls}">{icon} {status}</span>
          &nbsp;·&nbsp;{len(view_df)} routes monitored
        </div>
        """, unsafe_allow_html=True)

    # Threshold legend
    col_a, col_b, col_c, col_d = st.columns(4)
    for col, label, color, range_text in [
        (col_a, "🟢 Excellent", GREEN, "LTB < 10"),
        (col_b, "🟡 Good",      TEAL,  "LTB 10–20"),
        (col_c, "🟠 Warning",   AMBER, "LTB 20–30"),
        (col_d, "🔴 High/Critical", RED, "LTB ≥ 30"),
    ]:
        with col:
            st.markdown(f'<div style="font-size:.82rem;"><b style="color:{color};">{label}</b> — {range_text}</div>', unsafe_allow_html=True)

    st.markdown("")

    # Build display table
    display = view_df[["seller_name","route","daily_ltb","ltb_7d","ltb_14d","ltb_30d","shopping_count","order_count"]].copy()
    display.columns = ["Seller","Route","Daily LTB","7-Day LTB","14-Day LTB","30-Day LTB","Searches Today","Orders Today"]
    display = display.sort_values(active_col.replace("daily_ltb","Daily LTB").replace("ltb_7d","7-Day LTB").replace("ltb_14d","14-Day LTB").replace("ltb_30d","30-Day LTB"), ascending=False)

    # Colour format
    def color_ltb(val):
        if pd.isna(val): return "color:#9E9E9E"
        if val < 10: return "color:#2E7D32;font-weight:700"
        if val < 20: return "color:#00695C;font-weight:600"
        if val < 30: return "color:#E65100;font-weight:700"
        return "color:#C62828;font-weight:800"

    def highlight_row(row):
        ltb = row["Daily LTB"]
        if pd.isna(ltb): return [""] * len(row)
        if ltb >= 50:    return ["background-color:#FFEBEE"] * len(row)
        if ltb >= 30:    return ["background-color:#FFF3E0"] * len(row)
        if ltb < 10:     return ["background-color:#E8F5E9"] * len(row)
        return [""] * len(row)

    display["Seller"] = display["Seller"].str.split("(").str[0].str.strip()

    styled = display.style\
        .apply(highlight_row, axis=1)\
        .format({"Daily LTB":"{:.1f}","7-Day LTB":"{:.1f}","14-Day LTB":"{:.1f}","30-Day LTB":"{:.1f}","Searches Today":"{:,}","Orders Today":"{:,}"})\
        .map(color_ltb, subset=["Daily LTB","7-Day LTB","14-Day LTB","30-Day LTB"])

    st.dataframe(styled, use_container_width=True, height=480)

    # Export hint
    st.markdown("""
    <div class="callout-info" style="font-size:.82rem;">
      💡 <strong>Tip:</strong> Rows highlighted in <span style="color:#C62828;">red/orange</span> are being routed to Massive Search based on active rules.
      Green rows indicate high-converting sellers routed to Normal Search (Flex Pricer).
    </div>
    """, unsafe_allow_html=True)

    # Per-seller breakdown
    st.markdown("### 🔍 Seller LTB Comparison — All Windows")
    pivot_df = summary.groupby("seller_name")[["daily_ltb","ltb_7d","ltb_14d","ltb_30d"]].mean().round(2)
    pivot_df.columns = ["Daily","7-Day","14-Day","30-Day"]
    pivot_df.index = [n.split("(")[0].strip() for n in pivot_df.index]
    pivot_df = pivot_df.sort_values("Daily", ascending=False)

    fig_compare = go.Figure()
    colors_bar = [BLUE, TEAL, AMBER, RED]
    for i, col in enumerate(["Daily","7-Day","14-Day","30-Day"]):
        fig_compare.add_trace(go.Bar(
            name=col, x=pivot_df.index, y=pivot_df[col],
            marker_color=colors_bar[i], text=[f"{v:.1f}" for v in pivot_df[col]],
            textposition="outside",
        ))
    fig_compare.add_hline(y=30, line_dash="dash", line_color=RED, opacity=0.5,
                          annotation_text="Massive Search threshold (30)", annotation_position="right")
    fig_compare.update_layout(
        barmode="group", height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="Segoe UI",
        legend=dict(orientation="h", y=-0.15),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#E8EEF4", title="LTB Ratio"),
        margin=dict(l=10,r=10,t=10,b=60),
    )
    st.plotly_chart(fig_compare, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CHARTS & TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("""
    <div class="page-header">
      <h2>📈 Charts & Trends</h2>
      <p>30-day LTB trend analysis per seller and route</p>
      <div class="infosys-bar">
        <div class="inf-label">An</div>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 52" width="82" height="21">
          <text x="2" y="42" font-family="Arial Black,Arial,sans-serif" font-size="34"
                font-weight="900" fill="rgba(255,255,255,0.85)" letter-spacing="-1.5">infosys</text>
        </svg>
        <div class="inf-label">Travel &amp; Hospitality<br>Initiative</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        chart_seller = st.selectbox("Select Seller", list(SELLERS.keys()), key="chart_seller")
    with c2:
        chart_routes = st.multiselect("Select Routes", ROUTES, default=ROUTES[:4], key="chart_routes")

    if not chart_routes:
        st.info("Please select at least one route.")
    else:
        # --- Chart 1: LTB trend over 30 days ---
        st.markdown("### 📉 Daily LTB Trend — Last 30 Days")
        trend_df = df[
            (df["seller_name"] == chart_seller) &
            (df["route"].isin(chart_routes))
        ].copy()

        fig_trend = go.Figure()
        route_colors = px.colors.qualitative.Set2
        for i, route in enumerate(chart_routes):
            r_data = trend_df[trend_df["route"] == route].sort_values("date")
            if len(r_data) == 0: continue
            fig_trend.add_trace(go.Scatter(
                x=r_data["date"], y=r_data["daily_ltb"],
                name=route, mode="lines+markers",
                line=dict(color=route_colors[i % len(route_colors)], width=2.5),
                marker=dict(size=5),
            ))
        fig_trend.add_hline(y=30, line_dash="dash", line_color=RED, opacity=0.4,
                            annotation_text="Massive Search threshold")
        fig_trend.add_hline(y=10, line_dash="dot", line_color=GREEN, opacity=0.4,
                            annotation_text="Excellent threshold")
        fig_trend.update_layout(
            height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=-0.15),
            xaxis=dict(showgrid=True, gridcolor="#E8EEF4"),
            yaxis=dict(showgrid=True, gridcolor="#E8EEF4", title="LTB Ratio"),
            font_family="Segoe UI",
            hovermode="x unified",
            margin=dict(l=10,r=10,t=10,b=60),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        col_left, col_right = st.columns(2)
        with col_left:
            # --- Chart 2: Search vs Order volumes ---
            st.markdown("### 🔍 Searches vs Bookings (Last 7 Days)")
            recent = trend_df[trend_df["date"] >= pd.Timestamp(datetime.date.today() - datetime.timedelta(days=7))]
            vol_grp = recent.groupby("date")[["shopping_count","order_count"]].sum().reset_index()
            fig_vol = go.Figure()
            fig_vol.add_trace(go.Bar(name="Searches", x=vol_grp["date"], y=vol_grp["shopping_count"],
                                     marker_color=BLUE, opacity=0.85))
            fig_vol.add_trace(go.Bar(name="Bookings", x=vol_grp["date"], y=vol_grp["order_count"],
                                     marker_color=GREEN, opacity=0.85))
            fig_vol.update_layout(
                barmode="group", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", y=-0.18),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E8EEF4"),
                font_family="Segoe UI",
                margin=dict(l=10,r=10,t=10,b=55),
            )
            st.plotly_chart(fig_vol, use_container_width=True)

        with col_right:
            # --- Chart 3: Heatmap LTB by route ---
            st.markdown("### 🗺️ LTB Heatmap — Route × Window")
            seller_sum = summary[summary["seller_name"] == chart_seller]
            heat_routes = chart_routes[:8]
            heat_df = seller_sum[seller_sum["route"].isin(heat_routes)][["route","daily_ltb","ltb_7d","ltb_14d","ltb_30d"]].set_index("route")
            heat_df.columns = ["Daily","7-Day","14-Day","30-Day"]

            fig_heat = go.Figure(data=go.Heatmap(
                z=heat_df.values,
                x=heat_df.columns.tolist(),
                y=heat_df.index.tolist(),
                colorscale=[[0,"#E8F5E9"],[0.3,"#FFF9C4"],[0.6,"#FFCCBC"],[1,"#B71C1C"]],
                text=[[f"{v:.1f}" for v in row] for row in heat_df.values],
                texttemplate="%{text}",
                textfont={"size":12},
                showscale=True,
                colorbar=dict(title="LTB", thickness=14),
            ))
            fig_heat.update_layout(
                height=300, paper_bgcolor="rgba(0,0,0,0)",
                font_family="Segoe UI",
                margin=dict(l=10,r=10,t=10,b=10),
                xaxis=dict(side="top"),
            )
            st.plotly_chart(fig_heat, use_container_width=True)

    # --- Chart 4: All sellers comparison over time ---
    st.markdown("### 📊 All Sellers — Average LTB Trend (Last 30 Days)")
    all_trend = df.groupby(["date","seller_name"])["daily_ltb"].mean().reset_index()
    fig_all = go.Figure()
    seller_color_map = {k: v["color"] for k, v in SELLERS.items()}
    for seller in SELLERS:
        s_data = all_trend[all_trend["seller_name"] == seller].sort_values("date")
        fig_all.add_trace(go.Scatter(
            x=s_data["date"], y=s_data["daily_ltb"],
            name=seller.split("(")[0].strip(),
            mode="lines", line=dict(color=seller_color_map[seller], width=3),
        ))
    fig_all.add_hrect(y0=30, y1=80, fillcolor=RED, opacity=0.06, line_width=0,
                      annotation_text="Massive Search Zone", annotation_position="right")
    fig_all.add_hrect(y0=0, y1=10, fillcolor=GREEN, opacity=0.08, line_width=0,
                      annotation_text="Excellent Zone", annotation_position="right")
    fig_all.update_layout(
        height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.15),
        xaxis=dict(showgrid=True, gridcolor="#E8EEF4"),
        yaxis=dict(showgrid=True, gridcolor="#E8EEF4", title="Avg LTB Ratio"),
        font_family="Segoe UI",
        hovermode="x unified",
        margin=dict(l=10,r=10,t=10,b=60),
    )
    st.plotly_chart(fig_all, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — RULE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("""
    <div class="page-header">
      <h2>⚖️ Rule Engine — Routing Decision Control</h2>
      <p>ATPCO-style priority rules — first matching rule wins. No code changes needed.</p>
      <div class="infosys-bar">
        <div class="inf-label">An</div>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 52" width="82" height="21">
          <text x="2" y="42" font-family="Arial Black,Arial,sans-serif" font-size="34"
                font-weight="900" fill="rgba(255,255,255,0.85)" letter-spacing="-1.5">infosys</text>
        </svg>
        <div class="inf-label">Travel &amp; Hospitality<br>Initiative</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_rules, col_add = st.columns([1.4, 1])

    with col_rules:
        st.markdown("### 📋 Active Rules (Priority Order)")
        st.markdown("""
        <div class="callout-info" style="font-size:.82rem;margin-bottom:14px;">
          Rules are evaluated in <strong>priority order</strong> (lowest number first). 
          The <strong>first matching rule</strong> determines the routing action.
          Rule 99 is the default fallback.
        </div>
        """, unsafe_allow_html=True)

        for i, rule in enumerate(sorted(st.session_state["rules"], key=lambda r: r["priority"])):
            enabled_color = GREEN if rule.get("enabled") else "#9E9E9E"
            action_color  = RED if "Massive" in rule["action"] else GREEN
            status_icon   = "🟢" if rule.get("enabled") else "⚫"
            st.markdown(f"""
            <div class="rule-card" style="border-left:4px solid {enabled_color};">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <span style="font-weight:800;color:{BLUE};font-size:.82rem;">Priority {rule['priority']}</span>
                  &nbsp;{status_icon}&nbsp;
                  <span style="font-weight:700;font-size:.92rem;">{rule['name']}</span>
                </div>
                <span style="font-weight:800;color:{action_color};font-size:.85rem;">→ {rule['action']}</span>
              </div>
              <div style="margin-top:8px;font-size:.82rem;color:#64748B;">
                <span>👤 <b>Seller:</b> {rule['seller'].split('(')[0].strip() if '(' in rule['seller'] else rule['seller']}</span>
                &nbsp;&nbsp;
                <span>📐 <b>Condition:</b> LTB {rule['operator']} {rule['threshold']}</span>
                &nbsp;&nbsp;
                <span>📅 <b>Window:</b> {rule['window']}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns([1, 1])
            with c1:
                toggle_lbl = "Disable" if rule.get("enabled") else "Enable"
                if st.button(f"{toggle_lbl}", key=f"toggle_{rule['id']}", use_container_width=True):
                    for r in st.session_state["rules"]:
                        if r["id"] == rule["id"]:
                            r["enabled"] = not r.get("enabled", True)
                    st.rerun()
            with c2:
                if rule["priority"] != 99:
                    if st.button("🗑️ Delete", key=f"del_{rule['id']}", use_container_width=True):
                        st.session_state["rules"] = [r for r in st.session_state["rules"] if r["id"] != rule["id"]]
                        st.rerun()

    with col_add:
        st.markdown("### ➕ Add New Rule")
        with st.form("new_rule_form"):
            r_name     = st.text_input("Rule Name", placeholder="e.g. Block High LTB on DXB routes")
            r_priority = st.number_input("Priority", min_value=1, max_value=98, value=10)
            r_seller   = st.selectbox("Seller", ["All Sellers"] + list(SELLERS.keys()))
            r_window   = st.selectbox("LTB Window", ["Daily","7-Day Rolling","14-Day Rolling","30-Day Rolling"])

            st.markdown("**Condition: LTB...**")
            rc1, rc2 = st.columns(2)
            with rc1:
                r_op = st.selectbox("Operator", [">",">=","<","<="])
            with rc2:
                r_thresh = st.number_input("Threshold", min_value=0.0, max_value=200.0, value=30.0, step=1.0)

            r_action = st.radio("Routing Action", ["Massive Search","Normal Search"], horizontal=True)
            submitted = st.form_submit_button("✅ Add Rule", type="primary", use_container_width=True)
            if submitted and r_name:
                new_id = max([r["id"] for r in st.session_state["rules"]], default=0) + 1
                st.session_state["rules"].append({
                    "id": new_id, "priority": r_priority, "name": r_name,
                    "seller": r_seller, "operator": r_op, "threshold": r_thresh,
                    "window": r_window, "action": r_action, "enabled": True,
                })
                st.success(f"✅ Rule '{r_name}' added!")
                st.rerun()

        st.markdown("### 🔍 Live Routing Decision Simulator")
        st.markdown('<div class="callout-info" style="font-size:.82rem;">Enter any LTB ratio to see which rule fires and what routing decision is made.</div>', unsafe_allow_html=True)
        sim_seller = st.selectbox("Seller", list(SELLERS.keys()), key="sim_seller_sel")
        sim_ltb = st.slider("Simulated LTB Ratio", 1.0, 80.0, 25.0, 0.5)
        routing, rule_name = get_routing_decision(sim_ltb, st.session_state["rules"])
        r_color = RED if "Massive" in routing else GREEN
        r_icon  = "🚀" if "Massive" in routing else "✅"
        status, badge_cls, icon = get_ltb_status(sim_ltb)
        st.markdown(f"""
        <div style="background:{r_color}15;border:2px solid {r_color};border-radius:12px;padding:16px;margin-top:12px;text-align:center;">
          <div style="font-size:1.8rem;font-weight:900;color:{r_color};">{sim_ltb:.1f}:1</div>
          <div style="font-size:.8rem;color:#64748B;margin:4px 0;">Simulated LTB · {icon} {status}</div>
          <hr style="border:none;border-top:1px solid {r_color}30;margin:10px 0;">
          <div style="font-size:1.1rem;font-weight:800;color:{r_color};">{r_icon} {routing}</div>
          <div style="font-size:.78rem;color:#64748B;margin-top:4px;">Matched rule: <strong>{rule_name}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    # Routing decision table
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("### 🗺️ Live Routing Decisions — All Routes Today")
    routing_data = []
    for _, row in summary.iterrows():
        routing, rule_name = get_routing_decision(row["daily_ltb"], st.session_state["rules"])
        routing_data.append({
            "Seller": row["seller_name"].split("(")[0].strip(),
            "Route":  row["route"],
            "Daily LTB": row["daily_ltb"],
            "Routing Decision": routing,
            "Rule Applied": rule_name,
        })
    routing_df = pd.DataFrame(routing_data).sort_values("Daily LTB", ascending=False)

    def routing_style(row):
        if "Massive" in row["Routing Decision"]: return ["background:#FFF3E0"] * len(row)
        return ["background:#E8F5E9"] * len(row)

    styled_routing = routing_df.style\
        .apply(routing_style, axis=1)\
        .format({"Daily LTB": "{:.1f}"})\
        .map(lambda v: "color:#C62828;font-weight:700" if "Massive" in str(v) else "color:#2E7D32;font-weight:700", subset=["Routing Decision"])

    st.dataframe(styled_routing, use_container_width=True, height=360)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — AI INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("""
    <div class="page-header">
      <h2>🤖 AI Insights — Powered by Claude</h2>
      <p>Intelligent analysis and recommendations based on your LTB data and routing rules</p>
      <div class="infosys-bar">
        <div class="inf-label">An</div>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 52" width="82" height="21">
          <text x="2" y="42" font-family="Arial Black,Arial,sans-serif" font-size="34"
                font-weight="900" fill="rgba(255,255,255,0.85)" letter-spacing="-1.5">infosys</text>
        </svg>
        <div class="inf-label">Travel &amp; Hospitality<br>Initiative</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick suggestion cards (pre-built, no API needed)
    st.markdown("### ⚡ Automated Insights")

    worst_seller = summary.groupby("seller_name")["daily_ltb"].mean().idxmax()
    best_seller  = summary.groupby("seller_name")["daily_ltb"].mean().idxmin()
    worst_avg    = summary.groupby("seller_name")["daily_ltb"].mean().max()
    best_avg     = summary.groupby("seller_name")["daily_ltb"].mean().min()
    trending_up  = summary[summary["daily_ltb"] >= 40].groupby("route").size().idxmax() if len(summary[summary["daily_ltb"] >= 40]) > 0 else "N/A"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="callout-danger">
          <strong>🚨 Highest LTB Seller</strong><br>
          <strong>{worst_seller.split('(')[0].strip()}</strong> has an average LTB of
          <strong style="color:#C62828;">{worst_avg:.1f}:1</strong> today.
          All routes are being routed to Massive Search. Consider engaging this seller's team
          to understand why conversion is low.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="callout-success">
          <strong>✅ Best Performing Seller</strong><br>
          <strong>{best_seller.split('(')[0].strip()}</strong> is the most efficient with
          <strong style="color:#2E7D32;">{best_avg:.1f}:1</strong> average LTB.
          Operating on Normal Search — fast, cost-efficient processing.
          Use as a benchmark for other sellers.
        </div>
        """, unsafe_allow_html=True)
    with c3:
        high_ltb_routes = summary[summary["daily_ltb"] >= 30].shape[0]
        total_routes_n  = len(summary)
        pct = high_ltb_routes / total_routes_n * 100
        st.markdown(f"""
        <div class="callout-warn">
          <strong>⚠️ Routing Status</strong><br>
          <strong style="color:#E65100;">{high_ltb_routes} of {total_routes_n}</strong> route combinations
          ({pct:.0f}%) are currently being routed to Massive Search.
          Review the Rule Engine to check if thresholds are correctly calibrated.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # AI Chat Interface
    st.markdown("### 💬 Ask Claude — LTB Intelligence Assistant")

    # Build context for Claude
    def build_ltb_context():
        seller_summary = summary.groupby("seller_name").agg(
            avg_daily=("daily_ltb","mean"),
            avg_7d=("ltb_7d","mean"),
            routes=("route","count"),
            high_ltb_routes=("daily_ltb", lambda x: (x >= 30).sum()),
        ).round(2).to_string()

        top_worst = summary.sort_values("daily_ltb", ascending=False).head(5)[["seller_name","route","daily_ltb","ltb_7d"]].to_string()
        active_rules = [f"Priority {r['priority']}: {r['name']} — {r['seller'].split('(')[0].strip() if '(' in r['seller'] else r['seller']}, LTB {r['operator']} {r['threshold']} → {r['action']}" for r in st.session_state["rules"] if r.get("enabled")]

        return f"""
=== LTB Analytics Platform Context ===
Data date: {datetime.date.today()}
Total sellers: {len(SELLERS)}, Total routes: {len(ROUTES)}

SELLER SUMMARY:
{seller_summary}

TOP 5 WORST ROUTES TODAY:
{top_worst}

ACTIVE ROUTING RULES:
{chr(10).join(active_rules)}

Platform: Air Canada NDC 17.2
Routing options: Massive Search (broad inventory) vs Normal Search / Flex Pricer (efficient)
"""

    def call_claude(messages):
        api_key = st.session_state.get("anthropic_api_key", "")
        if not api_key:
            return "⚠️ Please enter your Anthropic API key in the sidebar to enable AI insights."
        try:
            system = """You are the LTB Analytics AI Assistant for Air Canada NDC.
You analyse Look-to-Book ratios and provide clear, actionable business recommendations.

ALWAYS keep responses concise (3-5 sentences max unless analysis is requested).
Speak in business terms — avoid technical jargon.
Always be specific — reference actual seller names and LTB values from the context.
Suggest concrete actions: adjust thresholds, engage sellers, review rules.
You understand: LTB = searches / bookings. Lower is better. High LTB → Massive Search routing."""

            payload = {"model":"claude-sonnet-4-20250514","max_tokens":600,"system":system,"messages":messages}
            data = json.dumps(payload).encode("utf-8")
            req  = urllib.request.Request("https://api.anthropic.com/v1/messages", data=data,
                headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"}, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())["content"][0]["text"]
        except Exception as e:
            return f"⚠️ API error: {str(e)[:100]}"

    # Display chat history
    chat_container = st.container()
    with chat_container:
        if not st.session_state["ai_messages"]:
            st.markdown("""
            <div class="callout-info">
              👋 <strong>Hello!</strong> I'm your LTB Intelligence Assistant powered by Claude.<br>
              I can analyse your seller data, explain routing decisions, suggest rule adjustments,
              and answer any questions about the Look-to-Book platform.<br><br>
              Try asking: <em>"Which seller needs the most attention?"</em> or 
              <em>"Should I adjust the Massive Search threshold?"</em>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state["ai_messages"]:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-bubble">🧑 {msg["display"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-bubble">🤖 {msg["display"]}</div>', unsafe_allow_html=True)

    # Quick question pills
    st.markdown("**Quick questions:**")
    q_cols = st.columns(4)
    quick_qs = [
        "Which seller needs the most attention right now?",
        "Is the 30-point Massive Search threshold correct?",
        "Which routes are performing best across all sellers?",
        "What action should I take for NDCConnect seller?",
    ]
    for i, (col, q) in enumerate(zip(q_cols, quick_qs)):
        with col:
            if st.button(q[:40]+"…" if len(q)>40 else q, key=f"qpill_{i}", use_container_width=True):
                ctx = build_ltb_context()
                user_content = f"[Context]\n{ctx}\n\n[Question]\n{q}"
                api_msgs = [{"role":m["role"],"content":m["content"]} for m in st.session_state["ai_messages"][-6:]]
                api_msgs.append({"role":"user","content":user_content})
                st.session_state["ai_messages"].append({"role":"user","display":q,"content":user_content})
                with st.spinner("Thinking…"):
                    reply = call_claude(api_msgs)
                st.session_state["ai_messages"].append({"role":"assistant","display":reply,"content":reply})
                st.rerun()

    # Text input
    with st.form("ai_chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask anything about your LTB data…",
                                   placeholder="e.g. Why is Travelport's LTB so high on YUL→DXB?",
                                   label_visibility="collapsed")
        c_send, c_clear = st.columns([4, 1])
        with c_send:
            send = st.form_submit_button("Send →", use_container_width=True, type="primary")
        with c_clear:
            clear = st.form_submit_button("🗑️ Clear", use_container_width=True)

    if clear:
        st.session_state["ai_messages"] = []
        st.rerun()

    if send and user_input.strip():
        ctx = build_ltb_context()
        user_content = f"[Context]\n{ctx}\n\n[Question]\n{user_input.strip()}"
        api_msgs = [{"role":m["role"],"content":m["content"]} for m in st.session_state["ai_messages"][-6:]]
        api_msgs.append({"role":"user","content":user_content})
        st.session_state["ai_messages"].append({"role":"user","display":user_input.strip(),"content":user_content})
        with st.spinner("Analysing LTB data…"):
            reply = call_claude(api_msgs)
        st.session_state["ai_messages"].append({"role":"assistant","display":reply,"content":reply})
        st.rerun()

    # Static analysis section
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("### 📋 AI-Generated Rule Suggestions")

    rule_suggestions = [
        {
            "priority": "HIGH",
            "title": "Create seller-specific rule for NDCConnect",
            "body": f"NDCConnect has the highest average LTB ({summary[summary['seller_code']=='ndcconnect']['daily_ltb'].mean():.1f}:1). Consider adding a seller-specific rule with threshold > 25 to ensure all their routes go to Massive Search regardless of other rules.",
            "action": "Add Rule: NDCConnect, LTB > 25, → Massive Search",
            "color": RED,
        },
        {
            "priority": "MEDIUM",
            "title": "Adjust default threshold from 30 to 25",
            "body": "The current 30:1 threshold means sellers with LTB between 25-30 go to Normal Search even though they are not converting efficiently. Lowering to 25 would catch more underperforming routes early.",
            "action": "Edit Rule: Default threshold, 30 → 25",
            "color": AMBER,
        },
        {
            "priority": "LOW",
            "title": "Add weekend LTB monitoring rule",
            "body": f"Sellers show significantly lower activity on weekends. A rolling 14-day window would smooth out this noise and give more stable routing decisions. Consider adding a 14-day rule for Travelport specifically.",
            "action": "Add Rule: Travelport, 14-day LTB > 20, → Massive Search",
            "color": BLUE,
        },
    ]

    for sug in rule_suggestions:
        priority_colors = {"HIGH": RED, "MEDIUM": AMBER, "LOW": BLUE}
        pc = priority_colors[sug["priority"]]
        st.markdown(f"""
        <div class="rule-card" style="border-left:4px solid {pc};">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <strong style="font-size:.92rem;">{sug['title']}</strong>
            <span style="background:{pc}20;color:{pc};padding:2px 10px;border-radius:10px;font-size:.72rem;font-weight:700;">{sug['priority']} PRIORITY</span>
          </div>
          <div style="font-size:.85rem;color:#374151;margin-bottom:8px;">{sug['body']}</div>
          <div style="font-size:.78rem;color:{pc};font-weight:600;">💡 Suggested action: {sug['action']}</div>
        </div>
        """, unsafe_allow_html=True)
