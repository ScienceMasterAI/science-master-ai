import streamlit as st
import google.generativeai as genai
from PIL import Image
import fitz  # PyMuPDF
from gtts import gTTS
import re
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Rasanga Science Legend AI", page_icon="🧬", layout="wide")

# Session State
if "user_points" not in st.session_state: st.session_state.user_points = 0
if "messages" not in st.session_state: st.session_state.messages = []

# Modern UI
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
.points-card { background: linear-gradient(45deg, #0ea5e9, #2563eb); padding: 15px; border-radius: 15px; text-align: center; font-weight: bold; }
.stButton>button { background: #38bdf8; color: #000; border-radius: 10px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- 2. AI SETUP (Version Force Fix) ---
def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("දෝෂයයි: Streamlit Secrets වල 'GEMINI_API_KEY' ඇතුළත් කර නැත.")
        st.stop()
    
    # මෙතන තමයි වැදගත්ම දේ: transport='rest' දාලා API එකට force කරනවා
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    
    # Model එක create කරනකොට system prompt එක ඇතුළෙන්ම දෙනවා
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="ඔබේ නම Rasanga Science Legend AI. නිර්මාතෘ Rasanga Kalamba arachchi. ශ්‍රී ලංකාවේ විෂය නිර්දේශයට අනුව සිංහලෙන් උගන්වන විද්‍යා ගුරුවරයෙකි."
    )
    return model

try:
    model = setup_ai()
except Exception as e:
    st.error(f"AI Setup Error: {str(e)}")

# --- 3. FUNCTIONS ---
def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        return " ".join([page.get_text() for page in doc])
    except: return "PDF කියවීමට නොහැක."

def generate_audio(text):
    try:
        clean_txt = re.sub(r'[^\u0D80-\u0DFF\s.]', '', text)
        if clean_txt.strip():
            tts = gTTS(text=clean_txt[:200], lang='si')
            tts.save("voice.mp3")
            return "voice.mp3"
    except: return None

# --- 4. UI & LOGIC ---
with st.sidebar:
    st.title("🧬 Science Pro")
    st.markdown(f"<div class='points-card'>🏆 ලකුණු: {st.session_state.user_points}</div>", unsafe_allow_html=True)
    mode = st.radio("අංශය:", ["AI සාකච්ඡාව", "🎯 විභාග Target", "🏆 Leaderboard"])
    uploaded_file = st.file_uploader("රූප සටහන් / PDF", type=["jpg", "png", "jpeg", "pdf"])
    if st.button("🗑️ Chat Clear"):
        st.session_state.messages = []
        st.rerun()

if mode == "AI සාකච්ඡාව":
    st.title("🎓 Rasanga Science Legend AI")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("ප්‍රශ්නය මෙතැන ලියන්න..."):
        st.session_state.user_points += 2
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            input_data = [prompt]
            if uploaded_file:
                if uploaded_file.type == "application/pdf":
                    input_data.append(f"PDF Content: {extract_text_from_pdf(uploaded_file)}")
                else:
                    input_data.append(Image.open(uploaded_file))

            try:
                # generate_content එකට force කරනවා stable version එකට
                response = model.generate_content(input_data)
                ans = response.text
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                
                audio = generate_audio(ans)
                if audio: st.audio(audio)
            except Exception as e:
                st.error(f"දෝෂයක්: {str(e)}")

elif mode == "🎯 විභාග Target":
    st.header("🎯 විභාග ඉලක්කගත ප්‍රශ්න")
    lesson = st.text_input("පාඩම:")
    if st.button("ප්‍රශ්නයක් හදන්න"):
        res = model.generate_content(f"{lesson} පාඩමට ප්‍රශ්නයක් සහ පිළිතුරු දෙන්න.")
        st.markdown(res.text)

else:
    st.header("🏆 Legend Leaderboard")
    st.write(f"ඔබේ ලකුණු මට්ටම: {st.session_state.user_points}")
