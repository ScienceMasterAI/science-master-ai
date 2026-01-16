import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time
import re
import io

# --- 1. API සහ මොඩල් සැකසුම් (Error Safe) ---
NEW_API_KEY = "AIzaSyChNlBP6nI1Ep35QN7rFMgyhym8o97c6fo" 
genai.configure(api_key=NEW_API_KEY)

def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        targets = ["models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-pro"]
        for target in targets:
            if target in available_models: return genai.GenerativeModel(target)
        return genai.GenerativeModel(available_models[0])
    except:
        return genai.GenerativeModel('gemini-pro')

model = get_working_model()

# --- 2. Gemini Style UI (Dark Mode) ---
st.set_page_config(page_title="Science Master Pro", page_icon="🔬", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    
    /* Input Bar Style with Icons */
    .stChatInputContainer {
        border-radius: 28px !important;
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
    }
    .stChatInputContainer::before {
        content: '➕  📷  🎙️';
        font-size: 18px;
        margin-right: 15px;
        color: #8e918f;
        display: flex;
        align-items: center;
        padding-left: 10px;
    }

    .main-title { color: #ffffff; font-size: 28px; font-weight: 500; text-align: center; margin-bottom: 20px; }
    [data-testid="stSidebar"] { background-color: #1e1f20; }
    .stMarkdown p { color: #e3e3e3 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar (Features & Safety) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    st.markdown("### 🛠️ පාලක පුවරුව")
    
    # විශේෂාංග තේරීම
    mode = st.radio("භාවිතා කරන ආකාරය:", 
                    ["Chat & Study", "Quick Quiz (ප්‍රශ්නාවලි)", "Study Planner (කාලසටහන්)"])
    
    st.write("---")
    uploaded_file = st.file_uploader("📷 රූප සටහන් / PDF ඇතුළත් කරන්න", type=["jpg", "png", "jpeg", "pdf"])
    
    # සංවාදය ගබඩා කිරීම (Save Chat)
    if st.session_state.messages:
        chat_data = ""
        for m in st.session_state.messages:
            role = "ඔබ" if m["role"] == "user" else "Science Master"
            chat_data += f"{role}: {m['content']}\n\n"
        
        st.download_button(
            label="📥 සංවාදය Save කරගන්න",
            data=chat_data,
            file_name="science_chat_backup.txt",
            mime="text/plain"
        )

    if st.button("🗑️ සංවාදය මකන්න (Clear)"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🔬 Science Master Pro AI</h1>", unsafe_allow_html=True)

# --- 4. විවිධ වැඩසටහන් (Modes) ක්‍රියාත්මක කිරීම ---

# A. Study Planner Mode
if mode == "Study Planner (කාලසටහන්)":
    st.subheader("📅 ඔබේ පාඩම් සැලසුම")
    exam_days = st.number_input("විභාගයට තව දින කීයක් තිබේද?", min_value=1, value=30)
    subjects = st.text_area("පාඩම් කළ යුතු මාතෘකා (පේළියෙන් පේළියට ලියන්න):")
    if st.button("සැලසුම සාදන්න"):
        with st.spinner("සකසමින්..."):
            res = model.generate_content(f"Create a study plan for {exam_days} days for these science topics: {subjects}. Explain in Sinhala.")
            st.markdown(res.text)

# B. Quick Quiz Mode
elif mode == "Quick Quiz (ප්‍රශ්නාවලි)":
    st.subheader("📝 විද්‍යා ප්‍රශ්නාවලිය")
    topic = st.text_input("ප්‍රශ්න ඇසිය යුතු මාතෘකාව ලියන්න:")
    if st.button("ප්‍රශ්න ලබාගන්න"):
        with st.spinner("ප්‍රශ්න සකසමින්..."):
            res = model.generate_content(f"Ask 3 MCQ science questions about {topic} in Sinhala with answers at the end.")
            st.markdown(res.text)

# C. Main Chat Mode (Chat & Past Paper Help)
else:
    # කලින් පණිවිඩ පෙන්වීම
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ප්‍රශ්නය ඇසීම
    if prompt := st.chat_input("ප්‍රශ්නය හෝ Past Paper ගැටලුව මෙතැන ලියන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            msg_holder = st.empty()
            try:
                # රූපයක් තිබේ නම් එය ඇතුළත් කිරීම
                if uploaded_file and uploaded_file.type != "application/pdf":
                    img = Image.open(uploaded_file)
                    response = model.generate_content([f"Explain clearly as a science teacher in Sinhala: {prompt}", img])
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

                # Voice (හඬ)
                clean_text = re.sub(r'[*()#\-_\[\]\n]', ' ', full_res)
                tts = gTTS(text=clean_text, lang='si')
                tts.save("speech.mp3")
                st.audio("speech.mp3")

            except Exception as e:
                st.error(f"දෝෂයක්: {e}")
