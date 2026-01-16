import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import time

# --- 1. API සැකසුම් ---
GOOGLE_API_KEY = "AIzaSyAzqgn6qnQHF28ck_a1uGD6CDSVqZEU28A"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. වැඩ කරන මොඩල් එකක් ස්වයංක්‍රීයව හඳුනාගැනීම ---
def get_safe_model():
    try:
        # පද්ධතියේ ඇති සියලුම මොඩල් ලැයිස්තුව ලබා ගනී
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # පිළිවෙලින් මේවා තිබේදැයි පරීක්ෂා කරයි
        for target in ["models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-pro"]:
            if target in available_models:
                return target
        return available_models[0] # කිසිවක් නැත්නම් පළමු මොඩල් එක ලබා දෙයි
    except:
        return "gemini-pro" # වැරදීමක් වුණොත් Default ලෙස gemini-pro ලබා දෙයි

# --- 3. UI සැකසුම් ---
st.set_page_config(page_title="Science Master AI", page_icon="🔬")
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🔬 Science Master AI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. Chat පෙන්වීම ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. ප්‍රශ්නය ඇතුළත් කිරීම ---
if prompt := st.chat_input("ප්‍රශ්නය මෙතැන ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        try:
            # ආරක්ෂිතව මොඩල් එක තෝරා ගනී
            working_model = get_safe_model()
            model = genai.GenerativeModel(working_model)
            
            # AI පිළිතුර ලබා ගැනීම
            response = model.generate_content(f"You are a science teacher. Explain in Sinhala: {prompt}")
            
            # Typing Effect
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.05)
                placeholder.markdown(full_res + "▌")
            
            placeholder.markdown(full_res)

            # Voice එකතු කිරීම
            tts = gTTS(text=full_res, lang='si')
            tts.save("s.mp3")
            st.audio("s.mp3")

            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.caption(f"භාවිතා කළේ: {working_model}")

        except Exception as e:
            st.error(f"දෝෂයක්: {e}")

# --- 6. රූප සටහන් විග්‍රහය ---
st.write("---")
with st.expander("🖼️ පින්තූරයක් Upload කරන්න"):
    up_img = st.file_uploader("Image", type=["jpg", "png"])
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=250)
        if st.button("විස්තර කරන්න"):
            model = genai.GenerativeModel(get_safe_model())
            res = model.generate_content(["Explain this science diagram in Sinhala:", img])
            st.info(res.text)
