import streamlit as st
import pandas as pd
from utils.market import get_market_data, MARKET_PRICES

CROP_EMOJIS = {
    "Tomato": "🍅", "Carrot": "🥕", "Cabbage": "🥬", "Brinjal": "🍆",
    "Leeks": "🌿", "Bitter Gourd": "🥒", "Capsicum": "🫑", "Pumpkin": "🎃",
    "Potato": "🥔", "Beetroot": "🫀", "Spinach": "🥬", "Radish": "🥕",
    "Banana": "🍌", "Papaya": "🍈", "Mango": "🥭", "Pineapple": "🍍",
    "Watermelon": "🍉", "Avocado": "🥑", "Guava": "🍐", "Passion Fruit": "🟣",
    "Cashew": "🥜", "Coconut": "🥥", "Groundnut": "🥜", "Macadamia": "🥜",
    "Rice": "🌾", "Maize": "🌽", "Soybean": "🌿",
}

def render(t):
    st.markdown(f"#### 📊 {t['marketTitle']}")
    crops = st.session_state.crops

    if not crops:
        st.markdown("""
        <div style='text-align:center;padding:2rem;background:#fff;border-radius:10px;
                    border:1px dashed #c8e6c9;color:#5a7a5a;font-size:13px'>
          Add crops to see market prices! 📊
        </div>
        """, unsafe_allow_html=True)
        st.markdown("#### 💹 All Market Prices (LKR/kg)")
        all_rows = [{"Crop": f"{CROP_EMOJIS.get(k,'🌱')} {k}", "Price (LKR/kg)": v}
                    for k, v in MARKET_PRICES.items()]
        st.dataframe(pd.DataFrame(all_rows), use_container_width=True, hide_index=True)
        return

    rows = get_market_data(crops)
    data = []
    for r in rows:
        emoji = CROP_EMOJIS.get(r["crop"], "🌱")
        data.append({
            "Crop": f"{emoji} {r['crop']}",
            "Price (LKR/kg)": f"Rs. {r['price']}",
            "Change": r["change"],
            "Est. Revenue": f"Rs. {r['revenue']:,}",
        })

    df = pd.DataFrame(data)

    def color_change(val):
        color = "#2d8a45" if val.startswith("+") else "#c0392b"
        return f"color: {color}; font-weight: bold"

    styled = df.style.applymap(color_change, subset=["Change"])
    st.dataframe(styled, use_container_width=True, hide_index=True)
