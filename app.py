import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time
import re

# --- 1. අලුත් API Key එක මෙතැනට දාන්න ---
# ඔයා අලුතින් හදාගත්ත Key එක පහත වරහන් ඇතුළේ පේස්ට් කරන්න
NEW_API_KEY = "AIzaSyChNlBP6nI1Ep35QN7rFMgyhym8o97c6fo" 

genai.configure(api_key=NEW_API_KEY)

def get_best_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
            if target in available_models: return target
        return available_models[0]
    except:
        return "gemini-pro"

model = genai.GenerativeModel(get_best_model())

# --- 2. UI සහ පෙනුම ---
st.set_page_config(page_title="Science Master AI", page_icon="🔬")

# Chat පිටුවේ Background සහ Bubbles හැඩගැන්වීම
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; }
    [data-testid="stChatMessage"]:nth-child(even) { background-color: #dcfce7 !important; border-radius: 15px; }
    [data-testid="stChatMessage"]:nth-child(odd) { background-color: #ffffff !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🔬 Science Master AI</h1>", unsafe_allow_html=True)

# සංවාදය පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ප්‍රශ්නය ඇසීම
if prompt := st.chat_input("ප්‍රශ්නය මෙතැන ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_holder = st.empty()
        full_res = ""
        try:
            response = model.generate_content(f"Explain in Sinhala: {prompt}")
            
            # Typing Effect
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.05)
                msg_holder.markdown(full_res + "▌")
            msg_placeholder = msg_holder.markdown(full_res)

            # Voice Cleaning (Special characters අයින් කර හඬ සැකසීම)
            clean_text = re.sub(r'[*()#\-_\[\]\n]', ' ', full_res)
            tts = gTTS(text=clean_text, lang='si')
            tts.save("speech.mp3")
            st.audio("speech.mp3")

            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"දෝෂයක්: {e}")
