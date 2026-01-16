import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time
import re

# --- 1. API සහ මොඩල් සැකසුම් ---
# මෙතැනට ඔයාගේ අලුත් API Key එක දාන්න
NEW_API_KEY = "AIzaSyChNlBP6nI1Ep35QN7rFMgyhym8o97c6fo" 
genai.configure(api_key=NEW_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 2. පිරිසිදු සහ නවීන පෙනුම (CSS) ---
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

st.markdown("""
    <style>
    /* මුළු පිටුවේම පසුබිම - තද පැහැති විද්‍යාත්මක පෙනුමක් */
    .stApp {
        background-color: #0f172a;
        color: #ffffff;
    }
    
    /* ප්‍රධාන මාතෘකාව */
    .main-title {
        color: #38bdf8;
        text-align: center;
        font-weight: bold;
        font-size: 35px;
        margin-bottom: 25px;
    }

    /* Chat Messages - අකුරු පැහැදිලිව පෙනීමට */
    [data-testid="stChatMessage"] {
        background-color: #1e293b !important; /* තද අළු පාට පසුබිම */
        border: 1px solid #334155;
        border-radius: 15px;
        color: #ffffff !important;
        margin-bottom: 12px;
    }

    /* User Message එක වෙනස් පාටකින් */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #334155 !important;
    }

    /* Input Box එක යටටම කර ලස්සන කිරීම */
    .stChatInputContainer {
        border-radius: 15px;
        background-color: #1e293b;
    }
    
    /* අකුරු වල පාට සුදු කිරීමට බල කිරීම */
    p, span, div {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)

# --- 3. Sidebar ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    st.write("---")
    if st.button("🗑️ Chat එක මකන්න"):
        st.session_state.messages = []
        st.rerun()

# --- 4. සංවාදය පෙන්වීම ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. ප්‍රශ්නය සහ පිළිතුර ---
if prompt := st.chat_input("ප්‍රශ්නය මෙතැන ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_holder = st.empty()
        
        try:
            # AI පිළිතුර
            response = model.generate_content(f"Explain as a teacher in Sinhala: {prompt}")
            full_res = response.text
            
            # Typing Effect
            displayed_text = ""
            for word in full_res.split():
                displayed_text += word + " "
                time.sleep(0.04)
                # අකුරු ටයිප් වන විට සුදු පාටින් පෙන්වීම
                msg_holder.markdown(f"<span style='color: white;'>{displayed_text}▌</span>", unsafe_allow_html=True)
            
            msg_holder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

            # Voice (හඬ)
            clean_text = re.sub(r'[*()#\-_\[\]\n]', ' ', full_res)
            tts = gTTS(text=clean_text, lang='si')
            tts.save("speech.mp3")
            st.audio("speech.mp3")

        except Exception as e:
            st.error(f"දෝෂයක්: {e}")
