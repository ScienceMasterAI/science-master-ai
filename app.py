import streamlit as st
import google.generativeai as genai

# API Key
GOOGLE_API_KEY = "AIzaSyAzqgn6qnQHF28ck_a1uGD6CDSVqZEU28A"
genai.configure(api_key=GOOGLE_API_KEY)

# මුලින්ම Page Config එක දාන්න
st.set_page_config(page_title="Science Master AI", page_icon="🔬")

st.title("🔬 Science Master AI")
st.write("Rasanga විසින් නිර්මාණය කරන ලදි.")

# වැඩ කරන මොඩල් එකක් ස්වයංක්‍රීයව තෝරාගැනීම
def get_working_model():
    try:
        # දැනට පාවිච්චි කරන්න පුළුවන් මොඩල් මොනවාදැයි පරීක්ෂා කිරීම
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # පිළිවෙලින් මේවා තිබේදැයි බලන්න
        for target in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]:
            if target in models:
                return target
        return models[0] if models else "gemini-pro"
    except:
        return "gemini-pro"

user_input = st.text_input("ඔබේ විද්‍යා ප්‍රශ්නය සිංහලෙන් ලියන්න:")

if st.button("පිළිතුර ලබාගන්න"):
    if user_input:
        with st.spinner('පිළිතුර සකස් කරමින් පවතී...'):
            try:
                model_name = get_working_model()
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content(f"Answer this science question in Sinhala: {user_input}")
                
                st.markdown("### 💡 පිළිතුර:")
                st.success(response.text)
                st.caption(f"භාවිතා කළේ: {model_name}")
            except Exception as e:
                st.error(f"දෝෂයක් සිදුවිය: {e}")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න.")
