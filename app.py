import streamlit as st
import google.generativeai as genai

# API Key
GOOGLE_API_KEY = "AIzaSyCTBR6jne5xmgcGE5eMHcxpsRxby3JKqKs"
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="Science Master AI", page_icon="🔬")
st.title("🔬 Science Master AI")

# වැඩ කරන මොඩල් එකක් හොයාගන්නා හැටි
def get_ai_response(text):
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            try:
                model = genai.GenerativeModel(m.name)
                response = model.generate_content(f"Answer in Sinhala: {text}")
                return response.text
            except:
                continue
    return "කරුණාකර මොහොතකින් නැවත උත්සාහ කරන්න."

user_input = st.text_input("ප්‍රශ්නය මෙතන ලියන්න:", "")

if st.button("පිළිතුර ලබාගන්න"):
    if user_input:
        with st.spinner('සකස් කරමින්...'):
            res = get_ai_response(user_input)
            st.write(res)
