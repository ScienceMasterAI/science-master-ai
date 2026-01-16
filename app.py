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

# 404 Error එක මඟහරවා ගැනීමට නිවැරදි මොඩල් එක තෝරාගැනීම
def get_working_model():
    models_to_try = [
        'gemini-1.5-flash-latest', 
        'gemini-1.5-flash', 
        'gemini-1.5-pro', 
        'gemini-pro'
    ]
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # මොඩල් එක වැඩද කියා පොඩි ටෙස්ට් එකක්
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            return model
        except:
            continue
    return genai.GenerativeModel('gemini-pro') # අන්තිම විසඳුම

def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# --- 2. UI SETUP ---
st.set_page_config(page_title="Science Master Pro", page_icon="🔬", layout="wide")

lottie_science = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_m6cu94kg.json")
lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_atlcl982.json")

st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .stButton>button { border-radius: 20px; background-color: #4285f4; color: white; width: 100%; }
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
    mode = st.radio("Mode එක තෝරන්න:", ["💬 Chat & Study", "📝 Interactive Quiz"])
    
    st.markdown("---")
    st.markdown(f'<div class="score-card"><h3>ලකුණු: {st.session_state.score}</h3></div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Reset All"):
        st.session_state.messages = []
        st.session_state.score = 0
        st.session_state.quiz_q = None
        st.rerun()

# --- 5. MAIN LOGIC ---
st.title("🔬 Science Master Pro AI")

if not setup_api():
    st.error("⚠️ කරුණාකර Streamlit Secrets වල 'GOOGLE_API_KEY' ඇතුළත් කරන්න!")
    st.stop()

model = get_working_model()

if mode == "💬 Chat & Study":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("ප්‍රශ්නය මෙතැන ලියන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(
