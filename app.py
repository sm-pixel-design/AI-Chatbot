import os
import streamlit as st
import google.generativeai as genai

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

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
# Initialize Generative AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat(history=[])

# Streamlit UI
st.sidebar.title("Chatbot")
st.sidebar.write("Hello, how can I help you?")
request = st.sidebar.text_input("Your message: ")
if(request):
    st.session_state.chat_started = True

if(st.session_state.chat_started):
    response = "Something went wrong!"  # default response
    try:
        api_response = chat.send_message(request)
        response = api_response.text
        pair = {'request':request, 'response':response}
        st.session_state.history.append(pair)

    except Exception as e:
        st.error(f"Error: {e}")

    for pair in st.session_state.history:
        st.info(pair['request'])   # to show prompts in a different color
        st.write(pair['response']) # to support markdowns