import streamlit as st
import google.generativeai as genai

# API Key
GOOGLE_API_KEY = "AIzaSyCTBR6jne5xmgcGE5eMHcxpsRxby3JKqKs"
genai.configure(api_key=GOOGLE_API_KEY)

# පිටුවේ පෙනුම
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .main-title { color: #1e3a8a; text-align: center; }
    .result-box { padding: 20px; background-color: white; border-radius: 15px; border-left: 5px solid #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>නිර්මාණකරු</h2>", unsafe_allow_html=True)
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", caption="Rasanga Kalamba Arachchi", use_container_width=True)
    st.markdown("<h3 style='text-align: center;'>Rasanga Kalamba Arachchi</h3>", unsafe_allow_html=True)
    st.info("විද්‍යා විෂය නිර්දේශය පිළිබඳ විශේෂඥ AI පද්ධතියකි.")

# AI Instruction
instruction = "You are Science Master AI by Rasanga. Explain science concepts deeply in Sinhala, relate to syllabus and past papers."

st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)
st.write("---")

user_input = st.text_area("ඔබේ විද්‍යා ගැටලුව මෙතන ලියන්න:", placeholder="උදා: ආලෝකයේ වර්තනය යනු කුමක්ද?")

if st.button("විශ්ලේෂණය කර පිළිතුර ලබාගන්න 🚀"):
    if user_input:
        with st.spinner('පිළිතුර සකස් කරමින්...'):
            try:
                # මෙතන මම පොඩි වෙනසක් කළා ලෙඩේ අයින් කරන්න
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{instruction}\n\nQuestion: {user_input}")
                
                st.markdown("### 💡 පිළිතුර:")
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                # ඇත්තම දෝෂය මොකක්ද කියලා බලාගන්න මේක උදවු වෙයි
                st.error(f"දෝෂයක් සිදුවිය. කරුණාකර නැවත උත්සාහ කරන්න. (Error: {str(e)})")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ලියන්න.")

st.write("---")
st.caption("© 2024 Rasanga Kalamba Arachchi")
