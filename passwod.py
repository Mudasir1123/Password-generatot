import streamlit as st
import requests
import random
import string
import google.generativeai as genai
import re
import os  # For environment variable handling

# 🔐 Configure Google Gemini AI API Key (Use environment variable for security)
GENAI_API_KEY = "AIzaSyBBTNFznyQOKaD56pYb-dXxwbp8bGYOXAI" 

# ✅ Ensure set_page_config() is the first Streamlit command!
st.set_page_config(page_title="🔐 AI Password Strength Checker", page_icon="🔑")

# Initialize Google Gemini AI API
genai.configure(api_key=GENAI_API_KEY)

# ✅ Use correct model name
MODEL_NAME = "gemini-1.5-flash"

# Password Generator API (Optional)
PASSWORD_API = "https://passwordwolf.com/api/?length=16&upper=on&lower=on&numbers=on&special=on"

# 🔑 Function to generate password based on strength level
def generate_password(strength):
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

# 🔎 Function to check password strength
def classify_password(password):
    if len(password) < 8:
        return "❌ Weak - Too short!"
    elif not (re.search(r"[A-Z]", password) and re.search(r"\d", password) and re.search(r"[!@#$%^&*()]")):
        return "⚠️ Medium - Needs uppercase, numbers, and special characters!"
    elif len(password) >= 12:
        return "✅ Strong - Secure password!"
    else:
        return "✅ Very Strong - Highly secure password!"

# 🤖 Function to improve password using AI
def improve_password_with_ai(password):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Improve this password to make it stronger and more secure: {password}"
        response = model.generate_content(prompt)

        # Extract AI response correctly
        if response and hasattr(response, "text"):
            return response.text.strip()
        else:
            return "⚠️ AI error: No response!"
    
    except Exception as e:
        return f"⚠️ AI error: {e}"

# 🤖 Function to interact with Gemini AI
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, "text") else "⚠️ AI error: No response!"
    except Exception as e:
        return f"❌ Error: {e}"

# 🎨 Streamlit UI
st.title("🔐 AI-Powered Password Strength Checker")

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
    st.markdown(f"**Password Strength:** {strength}")

    # Improve password dynamically
    with st.spinner("🔄 Improving password..."):
        improved_password = improve_password_with_ai(password_input)

    st.markdown(f"**🔒 AI Improved Password:** `{improved_password}`")

# 🤖 Ask Gemini AI Section
st.subheader("🤖 Ask AI (Gemini)")
user_prompt = st.text_input("Ask a question to Gemini AI:")

if st.button("Ask Gemini 🤖"):
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            gemini_response = ask_gemini(user_prompt)
        st.write(gemini_response)
    else:
        st.warning("⚠️ Please enter a question before clicking the button.")
