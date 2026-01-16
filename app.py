import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import fitz  # PyMuPDF
import re
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Science Master Pro AI", page_icon="🎓", layout="wide")

# API Key එක ආරක්ෂිතව ලබා ගැනීම
def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("කරුණාකර Streamlit Secrets වල 'GEMINI_API_KEY' ඇතුළත් කරන්න.")
        st.stop()
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # AI එකේ ස්වභාවය සහ දැනුම සීමාව තීරණය කිරීම
    system_instruction = (
        "ඔබ නම 'Science Master Pro' වේ. ඔබ ශ්‍රී ලංකාවේ විෂය නිර්දේශයට අනුව උගන්වන "
        "ප්‍රවීණ විද්‍යා ගුරුවරයෙකි. ඕනෑම සංකීර්ණ විද්‍යාත්මක ගැටලුවක් සිංහලෙන් සරලව "
        "පැහැදිලි කරන්න. රූප සටහන් සහ PDF ගොනු විශ්ලේෂණය කර පිළිතුරු ලබා දෙන්න."
    )
    
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction
    )

model = setup_ai()

# --- 2. FUNCTIONS ---
def extract_text_from_pdf(pdf_file):
    """PDF ගොනුවකින් අකුරු වෙන් කර ගැනීම"""
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"PDF කියවීමේ දෝෂයකි: {str(e)}"

def generate_audio(text):
    """සිංහල හඬ උත්පාදනය"""
    try:
        # සිංහල අකුරු පමණක් වෙන් කර ගැනීම
        clean_txt = re.sub(r'[^\u0D80-\u0DFF\s.]', '', text)
        if clean_txt.strip():
            tts = gTTS(text=clean_txt[:250], lang='si')
            tts.save("speech.mp3")
            return "speech.mp3"
    except:
        return None
    return None

# --- 3. UI LAYOUT ---
st.markdown("<h1 style='text-align: center;'>🎓 Science Master Pro AI</h1>", unsafe_allow_html=True)
st.write("---")

# Session State පවත්වා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("🔬 අධ්‍යයන මෙවලම්")
    uploaded_file = st.file_uploader("රූප සටහන් හෝ PDF (Past Papers) උඩුගත කරන්න", type=["jpg", "jpeg", "png", "pdf"])
    
    if st.button("🗑️ සංවාදය මකන්න"):
        st.session_state.messages = []
        st.rerun()

# --- 4. CHAT INTERACTION ---
# කලින් පණිවිඩ පෙන්වීම
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# පරිශීලකයාගේ ඇතුළත් කිරීම්
if prompt := st.chat_input("විද්‍යාව ගැටලුව මෙතැන ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_context = [prompt]
        
        # ගොනු පරීක්ෂාව
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                pdf_text = extract_text_from_pdf(uploaded_file)
                full_context.append(f"පහත දැක්වෙන්නේ මා ඇතුළත් කළ PDF ගොනුවේ අන්තර්ගතයයි: {pdf_text}")
            else:
                img = Image.open(uploaded_file)
                full_context.append(img)

        try:
            # AI පිළිතුර ලබා ගැනීම
            response = model.generate_content(full_context)
            final_text = response.text
            
            response_placeholder.markdown(final_text)
            st.session_state.messages.append({"role": "assistant", "content": final_text})
            
            # හඬ සහාය
            audio_path = generate_audio(final_text)
            if audio_path:
                st.audio(audio_path)
                
        except Exception as e:
            st.error(f"කණගාටුයි, දෝෂයක් සිදු විය: {str(e)}")
