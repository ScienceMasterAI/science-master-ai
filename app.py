import streamlit as st
import google.generativeai as genai

# 1. මුලින්ම API Key එක සැකසීම
GOOGLE_API_KEY = "AIzaSyAzqgn6qnQHF28ck_a1uGD6CDSVqZEU28A"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. පිටුවේ සැකසුම් (මෙය සැමවිටම මුලින්ම තිබිය යුතුය)
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

# Custom CSS - පෙනුම ලස්සන කිරීමට
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-title { color: #1e3a8a; text-align: center; font-weight: bold; font-size: 30px; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #1e3a8a; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar (පැති තීරුව) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>නිර්මාණකරු</h2>", unsafe_allow_html=True)
    try:
        st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    except:
        st.info("පින්තූරය පූරණය කළ නොහැක.")
    st.markdown("<p style='text-align: center; font-weight: bold;'>Rasanga Kalamba Arachchi</p>", unsafe_allow_html=True)
    st.markdown("---")

# --- ප්‍රධාන පිටුව ---
st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)
st.write("---")

user_input = st.text_area("ඔබේ විද්‍යා ප්‍රශ්නය සිංහලෙන් ලියන්න:", placeholder="උදා: සූර්ය බලශක්තිය නිපදවන්නේ කෙසේද?")

if st.button("විශ්ලේෂණය කර පිළිතුර ලබාගන්න 🚀"):
    if user_input:
        with st.spinner('පිළිතුර සකස් කරමින් පවතී...'):
            try:
                # වැඩ කරන මොඩල් එකක් තෝරා ගැනීම
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                instruction = "You are Science Master AI. Answer the question in Sinhala deeply as a teacher."
                response = model.generate_content(f"{instruction}\n\nQuestion: {user_input}")
                
                st.markdown("### 💡 පිළිතුර:")
                st.write(response.text)
            except Exception as e:
                st.error(f"දෝෂයක් සිදුවිය: {str(e)}")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න.")

st.markdown("---")
st.caption("© 2026 Science Master AI | Created by Rasanga")
