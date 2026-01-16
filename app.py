import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
from gtts import gTTS
import time

# --- 1. API සැකසුම් ---
GOOGLE_API_KEY = "AIzaSyAzqgn6qnQHF28ck_a1uGD6CDSVqZEU28A"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. පිටුවේ මූලික සැකසුම් ---
st.set_page_config(page_title="Science Master AI Pro", page_icon="🔬", layout="centered")

# පද්ධතියේ Chat History එක තබා ගැනීමට
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. UI එක හැඩගැන්වීම (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-title { color: #1e3a8a; text-align: center; font-weight: bold; font-size: 32px; margin-bottom: 20px; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🔬 Science Master AI Pro</h1>", unsafe_allow_html=True)

# --- 4. Sidebar (මෙවලම් තීරුව) ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    st.markdown("### Settings")
    theme = st.select_slider("පෙනුම (Theme):", options=["Light", "Dark"])
    language = st.radio("භාෂාව:", ["සිංහල", "English"])
    
    if st.button("සංවාදය මකන්න (Clear Chat)"):
        st.session_state.messages = []
        st.rerun()

# --- 5. Chat Interface (සංවාදය පෙන්වීම) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. ප්‍රශ්න ඇතුළත් කිරීමේ කොටස ---
if prompt := st.chat_input("ඔබේ විද්‍යා ගැටලුව මෙතැන ලියන්න..."):
    # පරිශීලකයාගේ ප්‍රශ්නය පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI පිළිතුර සකස් කිරීම
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # AI Model එක තෝරා ගැනීම
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # පද්ධතියට ලබා දෙන උපදෙස්
            instruction = "Explain as a science teacher in Sinhala." if language == "සිංහල" else "Explain as a science teacher in English."
            
            # පිළිතුර ලබා ගැනීම
            response = model.generate_content(f"{instruction}\nQuestion: {prompt}")
            
            # Typing Effect (අකුරෙන් අකුර පෙන්වීම)
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)

            # Voice - පිළිතුර ඇසීමට සැලැස්වීම
            tts_lang = 'si' if language == "සිංහල" else 'en'
            tts = gTTS(text=full_response, lang=tts_lang)
            tts.save("speech.mp3")
            st.audio("speech.mp3")

            # ඉතිහාසයට එකතු කිරීම
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"දෝෂයක්: {e}")

# --- 7. රූප සටහන් සහ PDF විග්‍රහය (අමතර මෙවලම්) ---
st.write("---")
with st.expander("🖼️ රූප සටහන් හෝ PDF හරහා ප්‍රශ්න අසන්න"):
    uploaded_img = st.file_uploader("රූප සටහනක් (Image) දමන්න", type=["jpg", "png", "jpeg"])
    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, width=300)
        if st.button("රූපය විග්‍රහ කරන්න"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(["Describe this science diagram in detail in Sinhala:", img])
            st.info(res.text)
