import streamlit as st
import google.generativeai as genai

# 1. ඔයාගේ API Key එක
GOOGLE_API_KEY = "Gen-lang-client-0882355738"

# 2. AI Setup
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# 3. App UI
st.set_page_config(page_title="Science Master AI", page_icon="🔬")

st.title("🔬 Science Master AI")
st.write("ඕනෑම විද්‍යා ගැටලුවක් සිංහලෙන් අහන්න!")

# 4. Chat logic
user_question = st.text_input("ඔබේ ගැටලුව මෙතන ලියන්න:")

if st.button("පිළිතුර ලබාගන්න"):
    if user_question:
        with st.spinner("පිළිතුර සොයමින් පවතී..."):
            try:
                full_prompt = f"Please answer the following science question in Sinhala: {user_question}"
                response = model.generate_content(full_prompt)
                st.success("මෙන්න පිළිතුර:")
                st.write(response.text)
            except Exception as e:
                st.error(f"පොඩි වැරදීමක් වුණා: {e}")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ලියන්න.")
