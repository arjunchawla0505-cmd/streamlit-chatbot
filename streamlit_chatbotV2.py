import os
import streamlit as st
import google.generativeai as genai

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load API key
if os.path.exists(".env"):
    # While running locally, load environment variables from .env
    from dotenv import load_dotenv
    load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    # While running on Streamlit, load API key from Streamlit secrets
    try:
        API_KEY = st.secrets["API_KEY"]
    except Exception:
        API_KEY = None
if not API_KEY:
    # If no API key is found, stop the app
    st.error("No API Key found!")
    st.stop()


genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

st.title(" AI Chatbot")



for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Type your message")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    response = model.generate_content(prompt)

    bot_reply = response.text

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

    with st.chat_message("assistant"):
        st.write(bot_reply)