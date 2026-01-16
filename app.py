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

# --- 2. AI SETUP (The Final Fix) ---
def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Secrets වල 'GEMINI_API_KEY' ඇතුළත් කර නැත.")
        st.stop()
    
    # මෙතනින් තමයි v1beta එක වෙනුවට v1 වලට බලෙන් හරවන්නේ
    os.environ["GOOGLE_API_USE_MTLS"] = "never" 
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    
    # Model එක හඳුන්වා දීම
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="ඔබේ නම Rasanga Science Legend AI. ඔබ ශ්‍රී ලංකාවේ විද්‍යා ගුරුවරයෙකි. සියල්ල සිංහලෙන් පැහැදිලි කරන්න."
    )
    return model

try:
    model = setup_ai()
except Exception as e:
    st.error(f"AI Setup Error: {str(e)}")

# --- 3. HELPER FUNCTIONS ---
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

# --- 4. UI ---
st.title("🎓 Rasanga Science Legend AI")

with st.sidebar:
    st.title("🧬 Science Pro")
    st.write(f"🏆 ලකුණු: {st.session_state.user_points}")
    uploaded_file = st.file_uploader("රූප සටහන් / PDF උඩුගත කරන්න", type=["jpg", "png", "jpeg", "pdf"])
    if st.button("🗑️ Chat Clear"):
        st.session_state.messages = []
        st.rerun()

# Chat display
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
            # ප්‍රධාන API ඇමතුම
            response = model.generate_content(input_data)
            ans = response.text
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            
            audio = generate_audio(ans)
            if audio: st.audio(audio)
        except Exception as e:
            st.error(f"දෝෂයක්: {str(e)}")
            st.info("සටහන: මෙම දෝෂය දිගටම එන්නේ නම් කරුණාකර App එක 'Reboot' කරන්න.")
