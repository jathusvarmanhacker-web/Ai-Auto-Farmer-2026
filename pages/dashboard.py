import streamlit as st
from datetime import datetime
from utils.market import MARKET_PRICES

CROP_EMOJIS = {
    "Tomato": "🍅", "Carrot": "🥕", "Cabbage": "🥬", "Brinjal": "🍆",
    "Leeks": "🌿", "Bitter Gourd": "🥒", "Capsicum": "🫑", "Pumpkin": "🎃",
    "Potato": "🥔", "Beetroot": "🫀", "Spinach": "🥬", "Radish": "🥕",
    "Banana": "🍌", "Papaya": "🍈", "Mango": "🥭", "Pineapple": "🍍",
    "Watermelon": "🍉", "Avocado": "🥑", "Guava": "🍐", "Passion Fruit": "🟣",
    "Cashew": "🥜", "Coconut": "🥥", "Groundnut": "🥜", "Macadamia": "🥜",
    "Rice": "🌾", "Maize": "🌽", "Soybean": "🌿",
}

STAGE_PCT = {"Seedling": 15, "Vegetative": 35, "Flowering": 55, "Fruiting": 75, "Harvesting": 95}
STAGE_COLORS = {
    "Seedling": "#81c784", "Vegetative": "#4caf50",
    "Flowering": "#f9a825", "Fruiting": "#ff7043", "Harvesting": "#2d8a45",
}

def get_greeting(t):
    h = datetime.now().hour
    if h < 12:
        return t["greetMorning"]
    elif h < 17:
        return t["greetAfternoon"]
    return t["greetEvening"]

def render(t):
    name = st.session_state.user_name.split()[0]
    location = st.session_state.user_location
    now = datetime.now().strftime("%A, %d %B")

    st.markdown(f"""
    <div style='background:linear-gradient(90deg,#1a5c2a,#2d8a45);color:#fff;border-radius:10px;
                padding:1rem 1.2rem;margin-bottom:1rem;display:flex;align-items:center;gap:10px'>
      <span style='font-size:28px'>🌿</span>
      <div>
        <div style='font-size:20px;font-weight:700'>{get_greeting(t)}, {name}!</div>
        <div style='font-size:12px;color:#a8d5b0'>{location} · {now}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Weather cards
    w = st.session_state.weather
    if w:
        c1, c2, c3, c4 = st.columns(4)
        for col, label_key, val_key, sub_key, icon in [
            (c1, "wlTemp",  "temp",     "temp_desc",     "🌡️"),
            (c2, "wlHum",   "humidity", "humidity_desc", "💧"),
            (c3, "wlRain",  "rain",     "rain_desc",     "🌧️"),
            (c4, "wlWind",  "wind",     "wind_desc",     "💨"),
        ]:
            with col:
                st.metric(label=f"{icon} {t[label_key]}", value=w[val_key], delta=w[sub_key])

    # Alert
    st.info(t["alertTip"])

    # Crops
    st.markdown(f"#### 🌾 {t['secCrops']}")
    crops = st.session_state.crops
    if not crops:
        st.markdown("""
        <div style='text-align:center;padding:1.5rem;background:#fff;border-radius:10px;
                    border:1px dashed #c8e6c9;color:#5a7a5a;font-size:13px'>
          No crops yet. Go to "My Crops" to add your first crop! 🌱
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, crop in enumerate(crops):
            emoji = CROP_EMOJIS.get(crop["type"], "🌱")
            pct = STAGE_PCT.get(crop["stage"], 50)
            color = STAGE_COLORS.get(crop["stage"], "#4caf50")
            with cols[i % 3]:
                st.markdown(f"""
                <div class='crop-card'>
                  <strong>{emoji} {crop['type']}</strong><br>
                  <span style='font-size:12px;color:#5a7a5a'>{crop['stage']} · {crop['area']} acres</span>
                  <div style='height:6px;border-radius:3px;background:#e8f5e9;margin:8px 0;overflow:hidden'>
                    <div style='height:100%;width:{pct}%;background:{color};border-radius:3px'></div>
                  </div>
                  <div style='font-size:10px;color:#5a7a5a;text-align:right'>{pct}%</div>
                </div>
                """, unsafe_allow_html=True)
