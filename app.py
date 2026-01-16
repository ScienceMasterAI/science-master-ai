import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_lottie import st_lottie
import requests
import time

# --- 1. CONFIGURATION & SECURITY ---
def setup_api():
    # Streamlit Secrets වලින් API Key එක ගනී
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# --- 2. UI SETUP ---
st.set_page_config(page_title="Science Master Pro", page_icon="🔬", layout="wide")

# Animations Load කිරීම
lottie_science = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_m6cu94kg.json")
lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_atlcl982.json")

# Custom CSS (Dark Theme Look)
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .stButton>button { border-radius: 20px; background-color: #4285f4; color: white; border: none; }
    .score-card { background: #1e1f20; padding: 15px; border-radius: 15px; border: 1px solid #4285f4; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "score" not in st.session_state: st.session_state.score = 0
if "quiz_q" not in st.session_state: st.session_state.quiz_q = None
if "answered" not in st.session_state: st.session_state.answered = False

# --- 4. SIDEBAR ---
with st.sidebar:
    if lottie_science: st_lottie(lottie_science, height=150)
    st.title("Settings")
    mode = st.radio("තෝරන්න:", ["💬 Chat & Study", "📝 Interactive Quiz"])
    
    st.markdown("---")
    st.markdown(f'<div class="score-card"><h3>ලකුණු: {st.session_state.score}</h3></div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Reset All"):
        st.session_state.messages = []
        st.session_state.score = 0
        st.session_state.quiz_q = None
        st.rerun()

# --- 5. LOGIC ---
st.title("🔬 Science Master Pro AI")

if not setup_api():
    st.error("⚠️ කරුණාකර Streamlit Secrets වල 'GOOGLE_API_KEY' ඇතුළත් කරන්න!")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

if mode == "💬 Chat & Study":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("ප්‍රශ්නය මෙතැන ලියන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("හිතමින් පවතිනවා..."):
                try:
                    response = model.generate_content(f"Explain as a science teacher in Sinhala: {prompt}")
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")

elif mode == "📝 Interactive Quiz":
    st.subheader("Interactive Quiz 🏆")
    q_topic = st.text_input("පාඩමේ නම ලියන්න:", "විද්‍යාව")

    if st.button("අලුත් ප්‍රශ්නයක් ගන්න"):
        with st.spinner("ප්‍රශ්නයක් හදනවා..."):
            prompt = f"Create a science MCQ about {q_topic} in Sinhala with 4 options (A, B, C, D). Mark correct answer as 'Correct: [Option]'."
            res = model.generate_content(prompt)
            st.session_state.quiz_q = res.text
            st.session_state.answered = False
            st.rerun()

    if st.session_state.quiz_q:
        q_text = st.session_state.quiz_q.split("Correct:")[0]
        st.info(q_text)
        ans = st.radio("පිළිතුර තෝරන්න:", ["A", "B", "C", "D"], index=None)
        
        if st.button("Check Answer") and not st.session_state.answered:
            st.session_state.answered = True
            correct_opt = st.session_state.quiz_q.split("Correct:")[-1].strip()
            if ans == correct_opt:
                st.session_state.score += 10
                st.success("නියමයි! ලකුණු 10ක් ලැබුණා.")
                if lottie_success: st_lottie(lottie_success, height=150)
                st.balloons()
            else:
                st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_opt}")
