import streamlit as st
import requests
import random
import string
import google.generativeai as genai
import re
import math
# 🔐 Configure Google Gemini AI API Key (Replace with a valid API key)
GENAI_API_KEY = "AIzaSyBBTNFznyQOKaD56pYb-dXxwbp8bGYOXAI"  # Replace with your real API key
# ✅ Set Streamlit Theme and Page Config
st.set_page_config(page_title="🔐 AI Password Strength Checker", page_icon="🔑", layout="centered")
custom_css = """
<style>
/* 🌌 Dark Theme with Neon Accents */
body, .stApp {
    background: linear-gradient(135deg, #D3A4D1, #6E3B6F);
    color: #FFFFFF;
    font-family: 'Poppins', sans-serif;
}
/* 💡 Headers with Neon Glow */
h1, h2, h3 {
    color: #FF6EC7;
    text-align: center;
    font-weight: 600;
    text-shadow: 0 0 10px #FF6EC7;
}
/* 🔘 Buttons with Neon Effect */
.stButton button {
    background: linear-gradient(135deg, #00E5FF, #FF6EC7) !important;
    color: #1F1C2C !important;
    border-radius: 8px;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.5);
}
.stButton button:hover {
    background: linear-gradient(135deg, #FF6EC7, #00E5FF) !important;
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(255, 110, 199, 0.7);
}
/* 📦 Input Fields with Glass Effect */
.stTextInput input {
    border: 1px solid #00E5FF;
    border-radius: 8px;
    background-color: rgba(31, 28, 44, 0.5);
    color: #E0E0E0;
    padding: 8px;
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
    backdrop-filter: blur(10px);
}
/* ⚠ Alerts with Glassmorphism */
.stAlert {
    border-left: 5px solid #FF6EC7;
    background-color: rgba(31, 28, 44, 0.7);
    color: #E0E0E0;
    box-shadow: 0 0 15px rgba(255, 110, 199, 0.3);
    backdrop-filter: blur(10px);
}
/* 🔄 Spinner with Neon Effect */
[data-testid="stSpinner"] {
    color: #FF6EC7 !important;
    text-shadow: 0 0 10px #FF6EC7;
}]
</style>
"""
# Apply the CSS to your Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)
# Initialize Google Gemini AI API
genai.configure(api_key=GENAI_API_KEY)
# ✅ Use correct model name
MODEL_NAME = "gemini-1.5-flash"
# 🔑 Function to generate password based on strength level
def generate_password(strength):
    try:
        if strength == "Weak":
            chars = string.ascii_lowercase
            length = random.randint(6, 8)
        elif strength == "Medium":
            chars = string.ascii_letters + string.digits
            length = random.randint(8, 10)
        elif strength == "Strong":
            chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+<>?"
            length = random.randint(12, 16)
        elif strength == "Very Strong":
            chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+<>?"
            length = random.randint(18, 24)
        else:
            return "Invalid strength level"
        return "".join(random.choice(chars) for _ in range(length))  
    except Exception as e:
        return f"⚠️ Error generating password: {e}"
# 🔎 Function to check password strength
def classify_password(password):
    try:
        if len(password) < 8:
            return "❌ Weak - Too short!"
        elif not (re.search(r"[A-Z]", password) and re.search(r"\d", password) and re.search(r"[!@#$%^&*()]", password)):
            return "⚠️ Medium - Needs uppercase, numbers, and special characters!"
        elif len(password) >= 12:
            return "✅ Strong - Secure password!"
        else:
            return "✅ Very Strong - Highly secure password!"
    except Exception as e:
        return f"⚠️ Error classifying password: {e}"
# 🔢 Function to calculate entropy (password strength in bits)
def calculate_entropy(password):
    try:
        char_sets = [
            (string.ascii_lowercase, 26),
            (string.ascii_uppercase, 26),
            (string.digits, 10),
            ("!@#$%^&*()-_=+<>?", 15)
        ]
        pool_size = sum(size for charset, size in char_sets if any(c in charset for c in password))
        entropy = math.log2(pool_size) * len(password) if pool_size > 0 else 0
        return round(entropy, 2)
    except Exception as e:
        return f"⚠️ Error calculating entropy: {e}"
# 🤖 Function to improve password using AI
def improve_password_with_ai(password):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Improve this password to make it stronger and more secure: {password}"
        response = model.generate_content(prompt)
        if response and hasattr(response, "text"):
            return response.text.strip()
        else:
            return "⚠️ AI error: No response!"
    except Exception as e:
        return f"⚠️ AI error: {e}"
# 🤖 Function to interact with Gemini AI chatbot
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, "text") else "⚠️ AI error: No response!"
    except Exception as e:
        return f"❌ Error: {e}"
# 🎨 Streamlit UI
st.title("🔐 AI-Powered Password Strength Checker & Chatbot")
# 🔑 Password Generator Section
st.subheader("🔑 Generate a Secure Password")
strength_level = st.selectbox("Select Password Strength:", ["Weak", "Medium", "Strong", "Very Strong"])
if st.button("Generate Password"):
    generated_password = generate_password(strength_level)
    st.session_state["generated_password"] = generated_password
    st.success(f"✅ Generated {strength_level} Password: `{generated_password}`")
# 📝 User Input Password Checker
st.subheader("📝 Enter Your Password to Check Strength")
password_input = st.text_input("Enter your password:", type="password", key="user_password")
if password_input:
    strength = classify_password(password_input)
    entropy = calculate_entropy(password_input)
    st.markdown(f"**Password Strength:** {strength}")
    st.markdown(f"🔢 **Entropy Score:** `{entropy} bits` (Higher is better)")
    # Improve password dynamically
    with st.spinner("🔄 Improving password..."):
        improved_password = improve_password_with_ai(password_input)
    st.markdown(f"**🔒 AI Improved Password:** `{improved_password}`")
# 🤖 Ask Gemini AI Chatbot Section
st.subheader("🤖 Ask AI (Gemini)")
user_prompt = st.text_input("Ask a question to Gemini AI:")
if st.button("Ask Gemini 🤖"):
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            gemini_response = ask_gemini(user_prompt)
        st.write(gemini_response)
    else:
        st.warning("⚠️ Please enter a question before clicking the button.")
