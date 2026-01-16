import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time
import re
import io

# --- 1. API සහ මොඩල් සැකසුම් ---
NEW_API_KEY = "AIzaSyChNlBP6nI1Ep35QN7rFMgyhym8o97c6fo" 
genai.configure(api_key=NEW_API_KEY)

# ආරක්ෂිතව මොඩල් එක තෝරාගැනීම
def get_model():
    try:
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return genai.GenerativeModel('gemini-pro')

model = get_model()

# --- 2. UI පෙනුම (Gemini Style CSS) ---
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

st.markdown("""
    <style>
    /* මුළු පිටුවේම පසුබිම */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    
    /* මාතෘකාව */
    .main-title {
        color: #ffffff;
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 30px;
        font-family: 'Google Sans', sans-serif;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        color: #e3e3e3 !important;
        border-radius: 20px;
    }

    /* --- Typing Bar එක මගේ එක වගේ හැඩගැන්වීම --- */
    .stChatInputContainer {
        border-radius: 30px !important;
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        padding: 5px 15px !important;
    }

    /* අයිකන් සඳහා විශේෂ පෙනුමක් ලබා දීම */
    .icon-bar {
        display: flex;
        gap: 15px;
        margin-top: -10px;
        margin-bottom: 10px;
        padding-left: 20px;
        color: #8e918f;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e1f20;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar සහ පින්තූර Upload එක ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    st.write("---")
    st.markdown("### 🖼️ පින්තූරයක් ඇතුළත් කරන්න")
    uploaded_image = st.file_uploader("රූප සටහන් විග්‍රහයට", type=["jpg", "png", "jpeg"])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. සංවාදය පෙන්වීම ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. අයිකන් පේළිය (Icons Bar) ---
# මෙතැන තමයි මගේ එකේ වගේ අයිකන් ටික පෙන්වන්නේ
st.markdown("""
    <div class="icon-bar">
        <span>📷 Image</span> | <span>🎙️ Voice</span> | <span>➕ More</span>
    </div>
    """, unsafe_allow_html=True)

# --- 6. ප්‍රශ්නය සහ පිළිතුර ---
if prompt := st.chat_input("මෙතැන ප්‍රශ්නය ලියන්න..."):
    # User පණිවිඩය
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI පිළිතුර
    with st.chat_message("assistant"):
        msg_holder = st.empty()
        
        try:
            # පින්තූරයක් තිබේදැයි බලමු
            if uploaded_image:
                img = Image.open(uploaded_image)
                response = model.generate_content([f"Explain this in Sinhala: {prompt}", img])
            else:
                response = model.generate_content(f"Explain clearly as a science teacher in Sinhala: {prompt}")
            
            full_res = response.text
            
            # Typing Effect
            displayed_text = ""
            for word in full_res.split():
                displayed_text += word + " "
                time.sleep(0.04)
                msg_holder.markdown(displayed_text + "▌")
            
            msg_holder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

            # Voice Processing
            clean_text = re.sub(r'[*()#\-_\[\]\n]', ' ', full_res)
            tts = gTTS(text=clean_text, lang='si')
            tts.save("speech.mp3")
            st.audio("speech.mp3")

        except Exception as e:
            st.error(f"Error: {e}")
