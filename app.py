import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=os.getenv("gemini_key"))

system_prompt = '''You are a medical advice assistant. Provide clear, accurate, and easy-to-understand health information based on general medical knowledge. 

You must:
- Explain possible causes, symptoms, and general care options in simple language.
- Encourage users to consult a qualified doctor for diagnosis, prescriptions, or serious symptoms.
- Ask relevant follow-up questions to better understand the user’s condition.
- Use a calm, empathetic, and non-judgmental tone.

You must NOT:
- Provide medical diagnoses or prescribe medications or dosages.
- Replace professional medical consultation.
- Make absolute or guaranteed claims.

If the user describes emergency symptoms (e.g., chest pain, difficulty breathing, severe bleeding, loss of consciousness, suicidal thoughts), clearly advise them to seek immediate medical help or contact local emergency services.
'''


if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(system_instruction=system_prompt))
st.title("Medical Bot")

#Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Display previous messages
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.write(msg)
# Input at bottom center
user_prompt = st.chat_input("Type your health question...")

if user_prompt:# Show user message
    st.session_state.history.append(("user", user_prompt))
    with st.chat_message("user"):
        st.write(user_prompt)
    try:
        response = st.session_state.chat.send_message(user_prompt)
        bot_text = response.text
    except Exception as e:
        bot_text = f"ERROR: {str(e)}"
# Show bot reply
    st.session_state.history.append(("assistant", bot_text))
    with st.chat_message("assistant"):
        st.write(bot_text)