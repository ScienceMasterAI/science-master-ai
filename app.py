import streamlit as st
import google.generativeai as genai
from streamlit_lottie import st_lottie
import requests

# --- 1. API එක ආරක්ෂිතව සැකසීම ---
def setup_api():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# --- 2. දැනට වැඩ කරන මොඩල් එකක් තෝරා ගැනීම (404 Error එක මඟහරී) ---
def get_working_model():
    # උත්සාහ කිරීමට මොඩල් ලැයිස්තුව (පිළිවෙලට)
    models_to_try = [
        'gemini-1.5-flash-latest',
        'gemini-1.5-flash',
        'gemini-1.5-pro-latest',
        'gemini-1.5-pro'
    ]
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # මොඩල් එක වැඩ දැයි පරීක්ෂා කිරීම (හරිම වැදගත්)
            model.generate_content("ping", generation_config={"max_output_tokens": 1})
            return model
        except:
            continue
    # කිසිවක් වැඩ නැත්නම් default එකක් ලබා දීම
    return genai.GenerativeModel('gemini-1.5-flash')

def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# --- 3. UI සැකසුම් ---
st.set_page_config(page_title="Science Master Pro", page_icon="🔬", layout="wide")

# Animations
lottie_science = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_m6cu94kg.json")
lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_atlcl982.json")

# Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .stButton>button { border-radius: 20px; background-color: #4285f4; color: white; width: 100%; border: none; }
    .score-card { background: #1e1f20; padding: 15px; border-radius: 15px; border: 1px solid #4285f4; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Session States
if "messages" not in st.session_state: st.session_state.messages = []
if "score" not in st.session_state: st.session_state.score = 0
if "quiz_q" not in st.session_state: st.session_state.quiz_q = None

# Sidebar
with st.sidebar:
    if lottie_science: st_lottie(lottie_science, height=150)
    st.title("පාලක පුවරුව")
    mode = st.radio("භාවිතා කරන ආකාරය:", ["💬 Chat & Study", "📝 Interactive Quiz"])
    st.markdown("---")
    st.markdown(f'<div class="score-card"><h3>ලකුණු: {st.session_state.score}</h3></div>', unsafe_allow_html=True)
    if st.button("🗑️ Reset"):
        st.session_state.messages = []
        st.session_state.score = 0
        st.rerun()

# --- 4. ප්‍රධාන ක්‍රියාකාරීත්වය ---
st.title("🔬 Science Master Pro AI")

if not setup_api():
    st.error("⚠️ කරුණාකර Streamlit Secrets වල 'GOOGLE_API_KEY' නිවැරදිව ඇතුළත් කරන්න!")
    st.stop()

# වැඩ කරන මොඩල් එක ලබා ගැනීම
try:
    model = get_working_model()
except Exception as e:
    st.error("පද්ධතියේ දෝෂයකි. පසුව උත්සාහ කරන්න.")
    st.stop()

if mode == "💬 Chat & Study":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("ඔබේ විද්‍යා ගැටලුව මෙතැන ලියන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("හිතමින් පවතිනවා..."):
                try:
                    response = model.generate_content(f"Explain as a science teacher in Sinhala: {prompt}")
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error("මොඩලය ප්‍රතිචාර දක්වන්නේ නැත. කරුණාකර වෙනත් ප්‍රශ්නයක් අසන්න.")

elif mode == "📝 Interactive Quiz":
    st.subheader("Science Quiz 🏆")
    if st.button("අලුත් ප්‍රශ්නයක් ගන්න"):
        with st.spinner("ප්‍රශ්නයක් සකසමින්..."):
            try:
                res = model.generate_content("Create a science MCQ in Sinhala with 4 options (A,B,C,D). Mark correct answer as 'Correct: [Option]'.")
                st.session_state.quiz_q = res.text
                st.rerun()
            except:
                st.error("ප්‍රශ්නය සැකසීමේදී දෝෂයක් ඇති විය.")

    if st.session_state.quiz_q:
        q_text = st.session_state.quiz_q.split("Correct:")[0]
        st.info(q_text)
        ans = st.radio("පිළිතුර:", ["A", "B", "C", "D"], index=None)
        if st.button("Check Answer"):
            correct = st.session_state.quiz_q.split("Correct:")[-1].strip()
            if ans and ans in correct:
                st.session_state.score += 10
                st.success("හරි! ලකුණු 10ක් ලැබුණා.")
                if lottie_success: st_lottie(lottie_success, height=150)
                st.balloons()
            else:
                st.error(f"වැරදියි! පිළිතුර: {correct}")
