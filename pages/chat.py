import streamlit as st
from utils.ai_chat import chat_with_ai

def render(t):
    st.markdown(f"#### 🤖 {t['aiTitle']}")
    st.markdown(f"""
    <span style='font-size:11px;padding:4px 10px;border-radius:20px;
                 background:#f5c518;color:#1a3d1f;font-weight:700;display:inline-block;margin-bottom:0.6rem'>
      {t['chatLangBadge']}
    </span>
    """, unsafe_allow_html=True)

    # Init history
    if not st.session_state.chat_history:
        welcome = t["chatWelcome"]
        st.session_state.chat_history = [{"role": "assistant", "content": welcome}]

    # Render chat history
    for msg in st.session_state.chat_history:
        with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
            st.write(msg["content"])

    # Input
    user_input = st.chat_input(t["chatPlaceholder"])
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("..."):
                try:
                    reply = chat_with_ai(
                        user_message=user_input,
                        history=st.session_state.chat_history[:-1],
                        user_name=st.session_state.user_name,
                        user_location=st.session_state.user_location,
                        user_acres=st.session_state.user_acres,
                        crops=st.session_state.crops,
                    )
                except Exception as e:
                    reply = f"⚠️ Could not connect to AI. Check your ANTHROPIC_API_KEY. ({e})"
            st.write(reply)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()
