import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time
import re
import os

# --- 1. API සහ මොඩල් සැකසුම් (Error handling සහිතව) ---
GOOGLE_API_KEY = "AIzaSyAzqgn6qnQHF28ck_a1uGD6CDSVqZEU28A"
genai.configure(api_key=GOOGLE_API_KEY)

def get_best_model():
    """වැඩ කරන මොඩල් එකක් ස්වයංක්‍රීයව තෝරාගැනීම"""
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ["models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-pro"]:
            if target in available_models:
                return target
        return available_models[0]
    except:
        return "gemini-pro"

# පද්ධතිය ආරම්භයේදීම මොඩල් එක තෝරාගනී
working_model_name = get_best_model()
model = genai.GenerativeModel(working_model_name)

# --- 2. පිටුවේ මූලික සැකසුම් ---
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. 🎨 CSS: පසුබිම සහ සංවාද පිටුව හැඩගැන්වීම ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #f1f5f9;
        background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
    }}
    .main-title {{
        color: #1e3a8a;
        text-align: center;
        font-weight: bold;
        font-size: 38px;
        text-shadow: 1px 1px 2px #94a3b8;
        padding: 10px;
    }}
    /* User Chat Bubble */
    [data-testid="stChatMessage"]:nth-child(even) {{
        background-color: #dcfce7 !important;
        border-radius: 15px 15px 2px 15px;
        border: 1px solid #bbf7d0;
    }}
    /* Assistant Chat Bubble */
    [data-testid="stChatMessage"]:nth-child(odd) {{
        background-color: #ffffff !important;
        border-radius: 15px 15px 15px 2px;
        border: 1px solid #e2e8f0;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. Sidebar ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    st.markdown("### ⚙️ Settings")
    lang = st.radio("ප්‍රතිචාර භාෂාව:", ["සිංහල", "English"])
    if st.button("🗑️ Chat එක මකන්න"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)

# --- 5. Chat ප්‍රදර්ශනය ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. සංවාදය මෙහෙයවීම ---
if prompt := st.chat_input("ප්‍රශ්නය මෙතැන ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_holder = st.empty()
        full_res = ""
        
        try:
            instruction = "Explain as a science teacher in Sinhala." if lang == "සිංහල" else "Explain as a science teacher in English."
            response = model.generate_content(f"{instruction}\nQuestion: {prompt}")
            
            # Typing Effect
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.05)
                msg_holder.markdown(full_res + "▌")
            msg_holder.markdown(full_res)

            # Voice Processing (පිරිසිදු කිරීම)
            clean_text = re.sub(r'[*()#\-_\[\]\n]', ' ', full_res)
            tts_lang = 'si' if lang == "සිංහල" else 'en'
            tts = gTTS(text=clean_text, lang=tts_lang)
            tts.save("speech.mp3")
            st.audio("speech.mp3")

            st.session_state.messages.append({"role": "assistant", "content": full_res})
        
        except Exception as e:
            st.error(f"දෝෂයක්: {e}")

# --- 7. රූප සටහන් විග්‍රහය ---
st.write("---")
with st.expander("🖼️ රූප සටහනක් හෝ පින්තූරයක් විග්‍රහ කරන්න"):
    up_img = st.file_uploader("Image Selection", type=["jpg", "png", "jpeg"])
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        if st.button("විස්තර කරන්න 🔎"):
            with st.spinner("විශ්ලේෂණය කරමින්..."):
                img_res = model.generate_content(["Describe this science diagram clearly in Sinhala:", img])
                st.info(img_res.text)
