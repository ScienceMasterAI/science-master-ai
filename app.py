import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time
import re  # අකුරු පිරිසිදු කිරීමට මෙය අවශ්‍ය වේ

# --- API සැකසුම් ---
genai.configure(api_key="AIzaSyAzqgn6qnQHF28ck_a1uGD6CDSVqZEU28A")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- පිටුවේ මූලික සැකසුම් ---
st.set_page_config(page_title="Science Master AI Pro", page_icon="🔬")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- පෙනුම සහ Theme (CSS) ---
st.markdown("""
    <style>
    .main-title { color: #1e3a8a; text-align: center; font-weight: bold; font-size: 35px; }
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar (මෙවලම්) ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    st.markdown("### 🛠️ පාලක පුවරුව")
    lang = st.radio("භාෂාව තෝරන්න:", ["සිංහල", "English"])
    if st.button("සංවාදය මකන්න (Clear Chat)"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🔬 Science Master AI Pro</h1>", unsafe_allow_html=True)

# --- Chat එක පෙන්වීම ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ප්‍රශ්න ඇසීම සහ පිළිතුරු ---
if prompt := st.chat_input("ඔබේ විද්‍යා ගැටලුව මෙතැන ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        full_res = ""
        
        try:
            instruction = "Explain as a science teacher in Sinhala." if lang == "සිංහල" else "Explain as a science teacher in English."
            response = model.generate_content(f"{instruction}\nQuestion: {prompt}")
            
            # 1. Typing Effect පෙන්වීම
            for chunk in response.text.split():
                full_res += chunk + " "
                time.sleep(0.05)
                msg_placeholder.markdown(full_res + "▌")
            
            msg_placeholder.markdown(full_res)

            # --- 2. හඬ සඳහා අකුරු පිරිසිදු කිරීම (Cleaning for Voice) ---
            # මෙහිදී *, (), #, - වැනි ලකුණු ඉවත් කරනු ලැබේ
            clean_text = re.sub(r'[*()#\-_\[\]]', '', full_res) 
            
            # Voice Generation
            tts_lang = 'si' if lang == "සිංහල" else 'en'
            tts = gTTS(text=clean_text, lang=tts_lang)
            tts.save("speech.mp3")
            st.audio("speech.mp3")

            st.session_state.messages.append({"role": "assistant", "content": full_res})

        except Exception as e:
            st.error(f"දෝෂයක්: {e}")

# --- 3. රූප සටහන් විග්‍රහය ---
st.write("---")
with st.expander("🖼️ රූප සටහනක් හෝ පින්තූරයක් ඇතුළත් කරන්න"):
    up_img = st.file_uploader("පින්තූරය තෝරන්න", type=["jpg", "png", "jpeg"])
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300, caption="ඔබ ලබා දුන් පින්තූරය")
        if st.button("විශ්ලේෂණය කරන්න 🔍"):
            with st.spinner("විශ්ලේෂණය කරමින් පවතී..."):
                res = model.generate_content(["Explain this clearly in Sinhala:", img])
                st.info(res.text)
