import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_lottie import st_lottie
import requests

# --- 1. CONFIGURATION & SECURITY ---
def setup_api():
    # Streamlit Secrets වලින් API Key එක ලබා ගැනීම
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# 404 Error එක මඟහරවා ගැනීමට සුදුසු මොඩල් එකක් තෝරාගැනීම
def get_working_model():
    models_to_try = [
        'gemini-1.5-flash-latest', 
        'gemini-1.5-flash', 
        'gemini-pro'
    ]
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # මොඩල් එක වැඩද කියා පරීක්ෂා කිරීමට කුඩා පණිවිඩයක් යැවීම
            model.generate_content("hi", generation_config={"max_output_tokens": 1})
            return model
        except:
            continue
    return genai.GenerativeModel('gemini-pro')

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

# Custom CSS (ලස්සන Dark Theme එකක් සඳහා)
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .stButton>button { border-radius: 20px; background-color: #4285f4; color: white; width: 100%; border: none; }
    .score-card { background: #1e1f20; padding: 15px; border-radius: 15px; border: 1px solid #4285f4; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE (දත්ත තබා ගැනීම) ---
if "messages" not in st.session_state: st.session_state.messages = []
if "score" not in st.session_state: st.session_state.score = 0
if "quiz_q" not in st.session_state: st.session_state.quiz_q = None
if "answered" not in st.session_state: st.session_state.answered = False

# --- 4. SIDEBAR ---
with st.sidebar:
    if lottie_science: st_lottie(lottie_science, height=150)
    st.title("පාලක පුවරුව")
    mode = st.radio("භාවිතා කරන ආකාරය:", ["💬 Chat & Study", "📝 Interactive Quiz"])
    
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
    st.error("⚠️ කරුණාකර Streamlit Cloud Secrets වල 'GOOGLE_API_KEY' ඇතුළත් කරන්න!")
    st.stop()

# වැඩ කරන මොඩල් එක ලබා ගැනීම
model = get_working_model()

if mode == "💬 Chat & Study":
    # පරණ පණිවිඩ පෙන්වීම
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # නව පණිවිඩයක් ඇතුළත් කිරීම
    if prompt := st.chat_input("ඔබේ විද්‍යා ගැටලුව මෙතැන ලියන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("හිතමින් පවතිනවා..."):
                try:
                    response = model.generate_content(f"Explain as a science teacher in Sinhala: {prompt}")
                    res_text = response.text
                    st.markdown(res_text)
                    st.session_state.messages.append({"role": "assistant", "content": res_text})
                except Exception as e:
                    st.error(f"Error: {e}")

elif mode == "📝 Interactive Quiz":
    st.subheader("Science Quiz 🏆")
    q_topic = st.text_input("පාඩමේ නම:", "විද්‍යාව")

    if st.button("අලුත් ප්‍රශ්නයක් ගන්න"):
        with st.spinner("ප්‍රශ්නයක් සකසමින්..."):
            prompt = f"Create a science MCQ about {q_topic} in Sinhala with 4 options (A, B, C, D). Clearly mark the correct option as 'Correct: [Option]' at the end."
            res = model.generate_content(prompt)
            st.session_state.quiz_q = res.text
            st.session_state.answered = False
            st.rerun()

    if st.session_state.quiz_q:
        # ප්‍රශ්නය සහ පිළිතුර වෙන් කර ගැනීම
        parts = st.session_state.quiz_q.split("Correct:")
        q_text = parts[0]
        st.info(q_text)
        
        ans = st.radio("පිළිතුර තෝරන්න:", ["A", "B", "C", "D"], index=None)
        
        if st.button("Check Answer") and not st.session_state.answered:
            st.session_state.answered = True
            correct_opt = parts[-1].strip() if len(parts) > 1 else "Unknown"
            
            if ans and ans in correct_opt:
                st.session_state.score += 10
                st.success(f"නියමයි! නිවැරදි පිළිතුර {correct_opt}. ඔබට ලකුණු 10ක් ලැබුණා.")
                if lottie_success: st_lottie(lottie_success, height=150)
                st.balloons()
            else:
                st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_opt}")
