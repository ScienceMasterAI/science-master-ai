import streamlit as st
import google.generativeai as genai
from PIL import Image
import fitz  # PyMuPDF
from gtts import gTTS
import re
import os

# --- 1. CONFIGURATION & MODERN THEME ---
st.set_page_config(page_title="Rasanga Science Legend AI", page_icon="🧬", layout="wide")

# Session State (දත්ත පවත්වාගෙන යාමට)
if "user_points" not in st.session_state: st.session_state.user_points = 0
if "messages" not in st.session_state: st.session_state.messages = []

# Premium UI පෙනුම සඳහා CSS
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
[data-testid="stSidebar"] { background-color: #1e293b; border-right: 2px solid #38bdf8; }
.points-card { background: linear-gradient(45deg, #0ea5e9, #2563eb); padding: 15px; border-radius: 15px; text-align: center; font-weight: bold; font-size: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
.stButton>button { background: #38bdf8; color: #000; border-radius: 10px; font-weight: bold; border: none; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- 2. AI SETUP ---
def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("කරුණාකර Streamlit Secrets වල 'GEMINI_API_KEY' ඇතුළත් කරන්න.")
        st.stop()
    
    # API එක නිවැරදිව configure කිරීම
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    system_prompt = (
        "ඔබේ නම Rasanga Science Legend AI වේ. ඔබේ නිර්මාතෘ Rasanga Kalamba arachchi වේ. "
        "ඔබ ශ්‍රී ලංකාවේ විද්‍යා ගුරුවරයෙකු ලෙස ඉතා සරලව සිංහලෙන් උගන්වන්න. "
        "රූප සටහන් සහ PDF විශ්ලේෂණය කර පැහැදිලි කරන්න. විභාග ප්‍රශ්න වලට Marking Scheme එකට අනුව පිළිතුරු දෙන්න."
    )

    # 404 Error එක මග හැරීමට මෙලෙස Model එක සකසන්න
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_prompt
    )

# AI සම්බන්ධ කිරීම
try:
    model = setup_ai()
except Exception as e:
    st.error(f"AI සම්බන්ධ වීමේ දෝෂයකි: {str(e)}")

# --- 3. HELPER FUNCTIONS ---
def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = " ".join([page.get_text() for page in doc])
        return text if text.strip() else "PDF එකේ අකුරු හඳුනාගත නොහැක."
    except:
        return "PDF කියවීමට නොහැක."

def generate_audio(text):
    try:
        # සිංහල අකුරු පමණක් වෙන් කර ගැනීම (gTTS සිංහල සඳහා)
        clean_txt = re.sub(r'[^\u0D80-\u0DFF\s.]', '', text)
        if clean_txt.strip():
            tts = gTTS(text=clean_txt[:200], lang='si')
            tts.save("voice.mp3")
            return "voice.mp3"
    except:
        return None
    return None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🧬 Rasanga Science Pro")
    st.markdown(f"<div class='points-card'>🏆 ලකුණු: {st.session_state.user_points}</div>", unsafe_allow_html=True)
    st.write("---")
    mode = st.radio("අංශය තෝරන්න:", ["AI සාකච්ඡාව", "🎯 විභාග Target ප්‍රශ්න", "🏆 Legend Leaderboard"])
    st.write("---")
    uploaded_file = st.file_uploader("රූප සටහන් / PDF (Past Papers)", type=["jpg", "png", "jpeg", "pdf"])
    
    if st.button("🗑️ සංවාදය මකන්න"):
        st.session_state.messages = []
        st.rerun()

# --- 5. APP MODES ---

# 🎯 TARGET QUESTIONS
if mode == "🎯 විභාග Target ප්‍රශ්න":
    st.header("🎯 විභාග ඉලක්කගත ප්‍රශ්න")
    lesson = st.text_input("පාඩමේ නම ලියන්න (උදා: ජෛව ක්‍රියාවලි):")
    if st.button("ප්‍රශ්න පත්‍රය සාදන්න"):
        st.session_state.user_points += 10
        with st.spinner("ප්‍රශ්න සකසමින්..."):
            res = model.generate_content(f"{lesson} පාඩමට අදාළව විභාගයට ඒමට හැකි ව්‍යුහගත රචනා ප්‍රශ්නයක් සහ පිළිතුරු සිංහලෙන් දෙන්න.")
            st.markdown(res.text)

# 🏆 LEADERBOARD
elif mode == "🏆 Legend Leaderboard":
    st.header("🏆 සයන්ස් ලෙජන්ඩ්ස් පුවරුව")
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.1); padding:20px; border-radius:10px;'>
    <p>🥇 1. <b>Rasanga Kalamba arachchi</b> - 5000 pts</p>
    <p>🥈 2. සචින්ත - 1250 pts</p>
    <p>🥉 3. <b>ඔබ (You)</b> - {st.session_state.user_points} pts</p>
    </div>
    """, unsafe_allow_html=True)

# 💬 CHAT MODE
else:
    st.title("🎓 Rasanga Science Legend AI")
    st.caption("ශ්‍රී ලංකාවේ විද්‍යා අධ්‍යාපනය සඳහා වූ AI සහකරු")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("විද්‍යාව ගැටලුව මෙතැන ලියන්න..."):
        st.session_state.user_points += 2
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            input_context = [prompt]
            
            # ගොනු විශ්ලේෂණය
            if uploaded_file:
                if uploaded_file.type == "application/pdf":
                    pdf_txt = extract_text_from_pdf(uploaded_file)
                    input_context.append(f"පහත PDF එකේ අන්තර්ගතය අනුව පිළිතුරු දෙන්න: {pdf_txt}")
                else:
                    img = Image.open(uploaded_file)
                    input_context.append(img)

            try:
                # මෙහිදී 'input_context' එක කෙලින්ම යැවිය හැක
                response = model.generate_content(input_context)
                ans = response.text
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                
                # හඬ සහාය
                audio_path = generate_audio(ans)
                if audio_path: st.audio(audio_path)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
