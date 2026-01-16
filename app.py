import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time
import re
import os

# --- 1. API සහ මොඩල් සැකසුම් ---
NEW_API_KEY = "AIzaSyB00XXs3rBT_fPpGWiuTEWSFYClJ0OiLag" 
genai.configure(api_key=NEW_API_KEY)

# ආරක්ෂිතව මොඩල් එක තෝරාගැනීම (404 Error එක මඟහරී)
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

# --- 2. Gemini Style UI (Dark Mode) ---
st.set_page_config(page_title="Science Master Pro", page_icon="🔬", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .main-title { color: #ffffff; font-size: 28px; font-weight: 500; text-align: center; margin-bottom: 20px; }
    
    /* Chat bubbles */
    [data-testid="stChatMessage"] { border-radius: 20px; margin-bottom: 10px; }
    
    /* Input Box styling */
    .stChatInputContainer { border-radius: 28px !important; background-color: #1e1f20 !important; border: 1px solid #444746 !important; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. Sidebar (මෙතන තමයි ඔක්කොම අයිකන් ටික තියෙන්නේ) ---
with st.sidebar:
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    st.markdown("### 🛠️ පාලක පුවරුව")
    
    # විශේෂාංග තේරීම
    mode = st.selectbox("භාවිතා කරන ආකාරය:", 
                       ["💬 Chat & Study", "📝 Quick Quiz", "📅 Study Planner"])
    
    st.write("---")
    st.markdown("📷 **පින්තූර / PDF ඇතුළත් කරන්න**")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg", "pdf"])
    
    st.write("---")
    # සංවාදය ගබඩා කිරීම
    if st.session_state.messages:
        chat_data = ""
        for m in st.session_state.messages:
            role = "ඔබ" if m["role"] == "user" else "Science Master"
            chat_data += f"{role}: {m['content']}\n\n"
        
        st.download_button(label="📥 සංවාදය Save කරගන්න", data=chat_data, file_name="chat_backup.txt", mime="text/plain")

    if st.button("🗑️ Chat එක මකන්න"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🔬 Science Master Pro AI</h1>", unsafe_allow_html=True)

# --- 4. Modes ක්‍රියාත්මක කිරීම ---

if mode == "📅 Study Planner":
    st.subheader("ඔබේ පාඩම් සැලසුම සාදමු")
    days = st.number_input("විභාගයට දින කීයක් තිබේද?", min_value=1)
    topics = st.text_area("පාඩම් ලැයිස්තුව ලියන්න:")
    if st.button("Plan එක හදන්න"):
        res = model.generate_content(f"Create a study plan for {days} days for: {topics} in Sinhala.")
        st.write(res.text)

elif mode == "📝 Quick Quiz":
    st.subheader("විද්‍යා ප්‍රශ්නාවලිය")
    q_topic = st.text_input("ප්‍රශ්න ඇසිය යුතු මාතෘකාව:")
    if st.button("ප්‍රශ්න ගන්න"):
        res = model.generate_content(f"Ask 3 MCQs about {q_topic} in Sinhala with answers.")
        st.write(res.text)

else: # Chat & Study Mode
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("ඔබේ විද්‍යා ගැටලුව මෙතැන ලියන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            msg_holder = st.empty()
            try:
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([f"Explain this in Sinhala: {prompt}", img])
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

                # Voice (හඬ)
                clean_text = re.sub(r'[*()#\-_\[\]\n]', ' ', full_res)
                tts = gTTS(text=clean_text, lang='si')
                tts.save("speech.mp3")
                st.audio("speech.mp3")
            except Exception as e:
                st.error(f"Error: {e}")
