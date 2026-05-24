import streamlit as st
import random

SCAN_RESULTS = [
    {
        "icon": "🍅",
        "name": "Tomato — Healthy",
        "desc": "No disease detected. Leaf color optimal. Continue regular schedule.",
        "badge": "✅ Healthy",
        "color": "#e8f5e9",
        "text_color": "#1a5c2a",
    },
    {
        "icon": "🥕",
        "name": "Carrot — Early Blight",
        "desc": "Early signs of blight detected. Apply copper-based fungicide. Reduce watering.",
        "badge": "⚠️ Warning",
        "color": "#fff9e6",
        "text_color": "#7a5a00",
    },
    {
        "icon": "🌾",
        "name": "Rice — Leaf Blast",
        "desc": "Blast fungus detected. Apply tricyclazole immediately. Isolate affected plants.",
        "badge": "🚨 Action Needed",
        "color": "#fdecea",
        "text_color": "#c0392b",
    },
]

def render(t):
    st.markdown(f"#### 🔬 {t['scanTitle']}")

    uploaded = st.file_uploader(
        "Upload a crop photo for AI analysis",
        type=["jpg", "jpeg", "png"],
        help="Take a photo of your crop leaves or plants",
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scan_clicked = st.button(
            f"📷 {t['scanBtnText']}",
            use_container_width=True,
            help=t["scanSubText"],
        )

    if uploaded:
        st.image(uploaded, caption="Uploaded crop image", use_container_width=True)

    if scan_clicked or uploaded:
        with st.spinner("🔍 Analysing crop..."):
            import time; time.sleep(1.2)
        result = random.choice(SCAN_RESULTS)

        st.markdown(f"#### 🔍 {t['scanResultTitle']}")
        st.markdown(f"""
        <div style='background:#fff;border-radius:10px;border:1px solid #c8e6c9;
                    padding:1rem;display:flex;gap:12px;align-items:flex-start'>
          <span style='font-size:36px'>{result['icon']}</span>
          <div>
            <h3 style='color:#1a5c2a;margin:0'>{result['name']}</h3>
            <p style='font-size:12px;color:#5a7a5a;margin:4px 0'>{result['desc']}</p>
            <span style='display:inline-block;padding:3px 10px;border-radius:20px;font-size:11px;
                         font-weight:700;background:{result['color']};color:{result['text_color']}'>
              {result['badge']}
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)
