import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time
import re

# --- 1. API සහ මොඩල් සැකසුම් ---
NEW_API_KEY = "AIzaSyChNlBP6nI1Ep35QN7rFMgyhym8o97c6fo" 
genai.configure(api_key=NEW_API_KEY)

def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        targets = ["models/gemini-1.5-flash", "models/gemini-pro"]
        for target in targets:
            if target in available_models: return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0])
    except:
        return genai.GenerativeModel('gemini-pro')

model = get_working_model()

# --- 2. Gemini Style UI (CSS) - අයිකන් පේන විදිහට ---
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    
    /* Input Bar එක මගේ එක වගේම හැඩගැන්වීම */
    .stChatInputContainer {
        border-radius: 28px !important;
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        padding-left: 10px !important;
    }

    /* Input එක ඇතුළේ පේන අයිකන් ටික (Fake Icons for UI look) */
    .stChatInputContainer::before {
        content: '➕  📷  🎙️'; /* මෙතන තමයි අයිකන් තියෙන්නේ */
        font-size: 18px;
        margin-right: 15px;
        color: #8e918f;
        display: flex;
        align-items: center;
        padding-left: 10px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #1e1f20; }
    .main-title { color: #ffffff; font-size: 24px; font-weight: 500; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. Sidebar ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    st.write("---")
    uploaded_file = st.file_uploader("📷 Upload Image / PDF", type=["jpg", "png", "jpeg", "pdf"])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 4. Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. Input සහ AI Response ---
if prompt := st.chat_input("Ask Science Master..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_holder = st.empty()
        try:
            # AI පිළිතුර
            if uploaded_file and uploaded_file.type != "application/pdf":
                img = Image.open(uploaded_file)
                response = model.generate_content([f"Explain as a science teacher in Sinhala: {prompt}", img])
            else:
                response = model.generate_content(f"Explain as a science teacher in Sinhala: {prompt}")
            
            full_res = response.text
            
            # Typing Effect
            displayed_text = ""
            for word in full_res.split():
                displayed_text += word + " "
                time.sleep(0.04)
                msg_holder.markdown(displayed_text + "▌")
            
            msg_holder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

            # Voice
            clean_text = re.sub(r'[*()#\-_\[\]\n]', ' ', full_res)
            tts = gTTS(text=clean_text, lang='si')
            tts.save("speech.mp3")
            st.audio("speech.mp3")

        except Exception as e:
            st.error(f"Error: {e}")
