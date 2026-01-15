import streamlit as st
import google.generativeai as genai

# ඔයාගේ API Key එක
GOOGLE_API_KEY = "AIzaSyCTBR6jne5xmgcGE5eMHcxpsRxby3JKqKs"

genai.configure(api_key=GOOGLE_API_KEY)

# මෙන්න මෙතන තමයි වෙනස කළේ
model = genai.GenerativeModel('gemini-1.0-pro')

st.set_page_config(page_title="Science Master AI", page_icon="🔬")

st.title("🔬 Science Master AI")
st.write("ඕනෑම විද්‍යා ගැටලුවක් සිංහලෙන් අහන්න!")

user_input = st.text_input("ඔබේ ගැටලුව මෙතන ලියන්න:", "")

if st.button("පිළිතුර ලබාගන්න"):
    if user_input:
        with st.spinner('පිළිතුර සකස් කරමින් පවතිී...'):
            try:
                # Prompt එක සිංහලෙන් පිළිතුරු දීමට සකස් කිරීම
                prompt = f"Please answer the following science question in clear Sinhala language: {user_input}"
                response = model.generate_content(prompt)
                
                st.subheader("පිළිතුර:")
                st.write(response.text)
                    
            except Exception as e:
                st.error(f"තාක්ෂණික දෝෂයක්: {e}")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න.")
