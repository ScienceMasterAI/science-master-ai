import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time
import re

# --- API සැකසුම් ---
# gemini-1.5-flash-latest භාවිතා කිරීමෙන් 404 දෝෂය මගහැරේ
GOOGLE_API_KEY = "AIzaSyAzqgn6qnQHF28ck_a1uGD6CDSVqZEU28A"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- පිටුවේ මූලික සැකසුම් ---
st.set_page_config(page_title="Science Master AI Pro", page_icon="🔬")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CSS ---
st.markdown("""
    <style>
    .main-title { color: #1e3a8a; text-align: center; font-weight: bold; font-size: 35px; }
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
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
            
            # Typing Effect
            for chunk in response.text.split():
                full_res += chunk + " "
                time.sleep(0.05)
                msg_placeholder.markdown(full_res + "▌")
            
            msg_placeholder.markdown(full_res)

            # --- Voice Cleaning (Special Characters ඉවත් කිරීම) ---
            # මෙහිදී *, (), #, _, -, සහ වරහන් සියල්ල ඉවත් කරයි
            clean_text = re.sub(r'[*()#\-_\[\]\n]', ' ', full_res) 
            
            tts_lang = 'si' if lang == "සිංහල" else 'en'
            tts = gTTS(text=clean_text, lang=tts_lang)
            tts.save("speech.mp3")
            st.audio("speech.mp3")

            st.session_state.messages.append({"role": "assistant", "content": full_res})

        except Exception as e:
            st.error(f"දෝෂයක්: {e}")
            st.info("කරුණාකර මොහොතකින් නැවත උත්සාහ කරන්න හෝ Reboot ලබා දෙන්න.")

# --- රූප සටහන් විග්‍රහය ---
st.write("---")
with st.expander("🖼️ රූප සටහනක් ඇතුළත් කරන්න"):
    up_img = st.file_uploader("Image", type=["jpg", "png", "jpeg"])
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        if st.button("විශ්ලේෂණය කරන්න"):
            res = model.generate_content(["Describe this science diagram in Sinhala:", img])
            st.info(res.text)
