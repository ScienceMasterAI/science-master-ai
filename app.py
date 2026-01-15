import streamlit as st
import google.generativeai as genai

# ඔයාගේ API Key එක
GOOGLE_API_KEY = "AIzaSyCTBR6jne5xmgcGE5eMHcxpsRxby3JKqKs"

genai.configure(api_key=GOOGLE_API_KEY)

# අලුත්ම සහ ස්ථිරම මොඩල් එක තෝරාගැනීම
model = genai.GenerativeModel('gemini-1.5-flash')

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
                
                if response.text:
                    st.subheader("පිළිතුර:")
                    st.write(response.text)
                else:
                    st.error("පිළිතුරක් ලබා ගැනීමට නොහැකි විය. කරුණාකර නැවත උත්සාහ කරන්න.")
                    
            except Exception as e:
                # මොඩල් එකේ නම වැරදි නම් මේකෙන් ඒක හදනවා
                st.error("පද්ධතියේ පොඩි දෝෂයක්. මම ඒක හදනවා...")
                try:
                    alt_model = genai.GenerativeModel('gemini-1.0-pro')
                    response = alt_model.generate_content(prompt)
                    st.subheader("පිළිතුර:")
                    st.write(response.text)
                except:
                    st.error(f"ඇත්තටම සමාවෙන්න, තාක්ෂණික දෝෂයක් ආවා: {e}")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න.")
