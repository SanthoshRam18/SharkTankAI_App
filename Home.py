import streamlit as st

# 🌃 Page setup
st.set_page_config(page_title="Shark Tank AI", layout="centered")

# 🎨 CSS to center elements
st.markdown("""
    <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 30px;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        .highlight {
            font-size: 40px;
            font-weight: bold;
            color: #ff4b2b;
            text-align: center;
            margin-top: 40px;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            margin-bottom: 30px;
            color: #cccccc;
        }
    </style>
""", unsafe_allow_html=True)

# 🏷️ Title and subtitle
st.markdown("<div class='highlight'>👋 Welcome to Shark Tank AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Pitch Your Future. Grab Your Deals.</div>", unsafe_allow_html=True)

# 🔤 Ask for name (mandatory)
user_name = st.text_input("👤 What's your name?", placeholder="Enter your name")

if user_name.strip():
    st.success(f"Welcome to the tank, **{user_name.strip()}**! 👋")

    # 🧑‍💼 Ask for role after name
    role = st.radio(
        "🧠 Who are you?",
        ["Investor", "Startup Founder"],
        horizontal=True,
        index=None
    )

    # ✅ Show proceed only after selecting role
    if role:
        with st.container():
            st.markdown("<div class='button-container'>", unsafe_allow_html=True)
            if st.button("🚀 Proceed"):
                st.session_state["user_name"] = user_name.strip()
                st.session_state["role"] = role
                st.switch_page("pages/app.py")
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("Please enter your name to continue.")
