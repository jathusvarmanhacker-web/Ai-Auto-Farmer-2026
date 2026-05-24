import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils.translations import T
from utils.weather import fetch_weather
from utils.market import get_market_data
from utils.ai_chat import chat_with_ai

st.set_page_config(
    page_title="AgroShield AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #1a3d1f !important; }
  [data-testid="stSidebar"] * { color: #a8d5b0 !important; }
  .stButton > button { background-color: #2d8a45; color: white; border-radius: 8px; border: none; font-weight: 600; }
  .stButton > button:hover { background-color: #1a5c2a; }
  .metric-card { background:#fff; border-radius:10px; padding:1rem; border:1px solid #c8e6c9; text-align:center; }
  .alert-box { background:#fff9e6; border:1.5px solid #f5c518; border-radius:10px; padding:0.9rem 1rem; margin-bottom:1rem; }
  .crop-card { background:#fff; border-radius:10px; padding:0.9rem; border:1px solid #c8e6c9; margin-bottom:0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
def init_state():
    defaults = {
        "lang": None,
        "logged_in": False,
        "user_name": "",
        "user_location": "Kandy, Sri Lanka",
        "user_acres": 2.4,
        "crops": [],
        "chat_history": [],
        "weather": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Language selection screen ─────────────────────────────────────────────────
if st.session_state.lang is None:
    st.markdown("""
    <div style='text-align:center; padding:3rem 0'>
      <div style='font-size:64px'>🌿</div>
      <h1 style='color:#1a5c2a; font-size:2.5rem; margin:0'>AgroShield AI</h1>
      <p style='color:#5a7a5a'>Smart Farming Assistant</p>
      <p style='color:#f5a000; font-weight:600; margin-top:1.5rem'>
        Choose your language / உங்கள் மொழியைத் தேர்வுசெய்க / ඔබේ භාෂාව තෝරන්න
      </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
    with col2:
        if st.button("🇬🇧  English", use_container_width=True):
            st.session_state.lang = "en"
            st.rerun()
    with col3:
        if st.button("🇮🇳  தமிழ்", use_container_width=True):
            st.session_state.lang = "ta"
            st.rerun()
    with col4:
        if st.button("🇱🇰  සිංහල", use_container_width=True):
            st.session_state.lang = "si"
            st.rerun()
    st.stop()

t = T[st.session_state.lang]

# ── Login screen ──────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown(f"""
        <div style='text-align:center; margin-bottom:1.5rem'>
          <div style='font-size:40px'>🌿</div>
          <h2 style='color:#1a5c2a; margin:0'>AgroShield AI</h2>
          <p style='color:#5a7a5a; font-size:13px'>{t['tagline']}</p>
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input(t["lbl_name"], placeholder="Suresh Perera")
        location = st.text_input(t["lbl_farm"], value="Kandy, Sri Lanka")
        acres = st.number_input(t["lbl_acres"], min_value=0.1, value=2.4, step=0.1)

        if st.button(t["loginBtn"], use_container_width=True):
            if name.strip():
                st.session_state.user_name = name.strip()
                st.session_state.user_location = location or "Kandy, Sri Lanka"
                st.session_state.user_acres = acres
                st.session_state.logged_in = True
                st.session_state.weather = fetch_weather(location)
                st.rerun()
            else:
                st.warning("Please enter your name.")

        st.markdown(f"""
        <div style='background:#f0fff4; border-left:4px solid #f5c518; border-radius:8px; padding:0.8rem; margin-top:1rem'>
          <strong style='color:#1a5c2a'>{t['setupTitle']}</strong><br>
          <span style='font-size:13px; color:#5a7a5a'>
            {t['q1']}<br>{t['q2']}<br>{t['q3']}
          </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← " + ("Change language" if st.session_state.lang == "en" else "மொழி மாற்று" if st.session_state.lang == "ta" else "භාෂාව වෙනස් කරන්න")):
            st.session_state.lang = None
            st.rerun()
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding:0.5rem 0 1rem'>
      <span style='font-size:24px'>🌿</span>
      <span style='color:#f5c518; font-weight:700; font-size:14px'> AgroShield AI</span><br>
      <span style='font-size:11px; color:#a8d5b0'>{t['sbTagline']}</span>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        f"🏠 {t['navDash']}": "dashboard",
        f"🌱 {t['navCrops']}": "crops",
        f"🔬 {t['navScan']}": "scanner",
        f"📊 {t['navMarket']}": "market",
        f"🤖 {t['navAI']}": "chat",
    }
    page = st.radio("", list(pages.keys()), label_visibility="collapsed")
    active_page = pages[page]

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:11px'>
      <strong style='color:#f5c518; display:block'>{t['sbFarmLabel']}</strong>
      {st.session_state.user_location}<br>
      {len(st.session_state.crops)} active crops
    </div>
    """, unsafe_allow_html=True)

# ── Pages ─────────────────────────────────────────────────────────────────────
if active_page == "dashboard":
    from pages.dashboard import render
    render(t)
elif active_page == "crops":
    from pages.crops import render
    render(t)
elif active_page == "scanner":
    from pages.scanner import render
    render(t)
elif active_page == "market":
    from pages.market import render
    render(t)
elif active_page == "chat":
    from pages.chat import render
    render(t)
