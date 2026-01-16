import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
from gtts import gTTS
import time
import os

# --- 1. API සැකසුම් ---
GOOGLE_API_KEY = "AIzaSyAzqgn6qnQHF28ck_a1uGD6CDSVqZEU28A"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. පිටුවේ මූලික සැකසුම් ---
st.set_page_config(page_title="Science Master AI Pro", page_icon="🔬", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. UI එක හැඩගැන්වීම ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-title { color: #1e3a8a; text-align: center; font-weight: bold; font-size: 32px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🔬 Science Master AI Pro</h1>", unsafe_allow_html=True)

# --- 4. Sidebar ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    language = st.radio("භාෂාව / Language:", ["සිංහල", "English"])
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. Chat Interface ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ඔබේ විද්‍යා ගැටලුව ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # මෙහි නම gemini-1.5-flash-latest ලෙස භාවිතා කිරීමෙන් 404 දෝෂය මගහැරේ
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            instruction = "Explain as a science teacher in Sinhala." if language == "සිංහල" else "Explain as a science teacher in English."
            response = model.generate_content(f"{instruction}\nQuestion: {prompt}")
            
            # Typing Effect
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.04)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)

            # Voice Generation
            tts_lang = 'si' if language == "සිංහල" else 'en'
            tts = gTTS(text=full_response, lang=tts_lang)
            tts.save("speech.mp3")
            st.audio("speech.mp3")

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            # 404 Error එකක් ආවොත් පරණ gemini-pro එකට මාරු වීම
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except:
                st.error(f"දෝෂයක් සිදුවිය: {e}")

# --- 6. රූප සටහන් විග්‍රහය ---
st.write("---")
with st.expander("🖼️ රූප සටහනක් Upload කරන්න"):
    uploaded_img = st.file_uploader("රූපය තෝරන්න", type=["jpg", "png", "jpeg"])
    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, width=250)
        if st.button("රූපය විග්‍රහ කරන්න"):
            # රූප සඳහාද Flash-Latest භාවිතා කිරීම
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            res = model.generate_content(["Describe this science diagram in Sinhala:", img])
            st.info(res.text)
