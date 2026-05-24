import streamlit as st
from datetime import date

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

ALL_CROPS = {
    "🥦 Vegetables": ["Tomato", "Carrot", "Cabbage", "Brinjal", "Leeks", "Bitter Gourd",
                      "Capsicum", "Pumpkin", "Potato", "Beetroot", "Spinach", "Radish"],
    "🍎 Fruits": ["Banana", "Papaya", "Mango", "Pineapple", "Watermelon",
                  "Avocado", "Guava", "Passion Fruit"],
    "🥜 Nuts": ["Cashew", "Coconut", "Groundnut", "Macadamia"],
    "🌾 Grains": ["Rice", "Maize", "Soybean"],
}
FLAT_CROPS = [c for crops in ALL_CROPS.values() for c in crops]
STAGES = ["Seedling", "Vegetative", "Flowering", "Fruiting", "Harvesting"]

def render(t):
    st.markdown(f"#### 🌱 {t['cropsTitle']}")

    with st.expander(t["addCropBtn"], expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            crop_type = st.selectbox(t["lblCropType"], FLAT_CROPS)
            area = st.number_input(t["lblArea"], min_value=0.1, value=0.5, step=0.1)
        with col2:
            stage = st.selectbox(t["lblStage"], STAGES)
            planted = st.date_input(t["lblPlanted"], value=date.today())

        if st.button("Add Crop ✓"):
            st.session_state.crops.append({
                "type": crop_type,
                "stage": stage,
                "area": area,
                "date": str(planted),
                "id": len(st.session_state.crops),
            })
            st.success(f"Added {crop_type} 🌱")
            st.rerun()

    crops = st.session_state.crops
    if not crops:
        st.markdown("""
        <div style='text-align:center;padding:2rem;background:#fff;border-radius:10px;
                    border:1px dashed #c8e6c9;color:#5a7a5a;font-size:13px'>
          No crops added yet. Click "Add Crop" to begin! 🌱
        </div>
        """, unsafe_allow_html=True)
        return

    cols = st.columns(3)
    to_remove = None
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
            if st.button("🗑 Remove", key=f"remove_{i}"):
                to_remove = i

    if to_remove is not None:
        st.session_state.crops.pop(to_remove)
        st.rerun()
