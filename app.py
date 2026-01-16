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

# වැඩ කරන මොඩල් එකක් තෝරාගැනීම
def get_best_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ["models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-pro"]:
            if target in available_models: return target
        return available_models[0]
    except:
        return "gemini-pro"

model = genai.GenerativeModel(get_best_model())

# --- 2. UI පෙනුම සහ Background ---
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

st.markdown("""
    <style>
    /* පිටුවේ පසුබිම (Background) */
    .stApp {
        background-color: #f0f4f8;
        background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
    }
    /* මාතෘකාව */
    .main-title {
        color: #1e3a8a;
        text-align: center;
        font-weight: bold;
        font-size: 38px;
        margin-bottom: 20px;
    }
    /* Chat Bubbles */
    [data-testid="stChatMessage"]:nth-child(even) { background-color: #e0f2fe !important; border-radius: 15px; }
    [data-testid="stChatMessage"]:nth-child(odd) { background-color: #ffffff !important; border-radius: 15px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)

# --- 3. Sidebar ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    if st.button("🗑️ සංවාදය මකන්න"):
        st.session_state.messages = []
        st.rerun()

# --- 4. සංවාදය පෙන්වීම (Display Chat History) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. ප්‍රශ්නය ඇසීම සහ පිළිතුර ලබාදීම ---
if prompt := st.chat_input("ප්‍රශ්නය මෙතැන ලියන්න..."):
    # User message එක සේව් කර පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant පිළිතුර
    with st.chat_message("assistant"):
        msg_holder = st.empty() # අකුරු ටයිප් වෙන තැන
        
        try:
            # AI එකෙන් පිළිතුර ලබා ගැනීම
            response = model.generate_content(f"Explain clearly as a science teacher in Sinhala: {prompt}")
            full_res = response.text
            
            # Typing Effect (අකුරෙන් අකුර පෙන්වීම)
            displayed_text = ""
            for word in full_res.split():
                displayed_text += word + " "
                time.sleep(0.05)
                msg_holder.markdown(displayed_text + "▌")
            
            # අවසාන පිළිතුර ස්ථිරව පෙන්වීම
            msg_holder.markdown(full_res)

            # සංවාද ඉතිහාසයට පිළිතුර ඇතුළත් කිරීම (මෙය වැදගත්!)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

            # Voice Processing (හඬ සැකසීම)
            clean_text = re.sub(r'[*()#\-_\[\]\n]', ' ', full_res)
            tts = gTTS(text=clean_text, lang='si')
            tts.save("speech.mp3")
            st.audio("speech.mp3")

        except Exception as e:
            st.error(f"දෝෂයක්: {e}")

# --- 6. රූප සටහන් විග්‍රහය ---
st.write("---")
with st.expander("🖼️ රූප සටහනක් Upload කර විස්තර අහන්න"):
    up_img = st.file_uploader("Image Selection", type=["jpg", "png", "jpeg"])
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        if st.button("විශ්ලේෂණය කරන්න"):
            res = model.generate_content(["Explain this science diagram in Sinhala:", img])
            st.info(res.text)
