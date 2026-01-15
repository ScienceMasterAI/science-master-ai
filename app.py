import streamlit as st
import google.generativeai as genai

# API Key - මම ඔයා දීපු Key එකම පාවිච්චි කරනවා
GOOGLE_API_KEY = "AIzaSyCTBR6jne5xmgcGE5eMHcxpsRxby3JKqKs"
genai.configure(api_key=GOOGLE_API_KEY)

# පිටුවේ පෙනුම
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

# Custom CSS - පෙනුම තවත් ලස්සන කරන්න
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-title { color: #1e3a8a; text-align: center; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #1e3a8a; color: white; }
    .sidebar-name { text-align: center; font-weight: bold; color: #1e3a8a; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar (පැති තීරුව) - ඔයාගේ ෆොටෝ එක සහ නම ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>නිර්මාණකරු</h2>", unsafe_allow_html=True)
    
    # ඔයාගේ පින්තූරය - මම මේ ලින්ක් එක පරීක්ෂා කළා, මේක වැඩ කරන්න ඕනේ
    try:
        st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    except:
        st.warning("පින්තූරය පූරණය වීමේ දෝෂයකි.")
        
    st.markdown("<p class='sidebar-name'>Rasanga Kalamba Arachchi</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Science Master AI නිර්මාණකරු</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("විෂය නිර්දේශයට අනුව ඕනෑම විද්‍යා ගැටලුවක් මෙතැනින් අහන්න.")

# --- ප්‍රධාන පිටුව ---
st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)
st.write("---")

# දැනුම පද්ධතිය (Past Papers සහ Syllabus ගැන උපදෙස්)
instruction = "You are Science Master AI by Rasanga. Explain science concepts deeply in Sinhala, relate to the syllabus and mention past paper tips."

user_input = st.text_area("ඔබේ විද්‍යා ප්‍රශ්නය සිංහලෙන් ලියන්න:", placeholder="උදා: න්‍යෂ්ටික විලයනය යනු කුමක්ද?")

if st.button("විශ්ලේෂණය කර පිළිතුර ලබාගන්න 🚀"):
    if user_input:
        with st.spinner('පිළිතුර සකස් කරමින් පවතී...'):
            try:
                # වැඩ කරන මොඩල් එකක් ස්වයංක්‍රීයව තෝරාගැනීම
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model_name = available_models[0] if available_models else "gemini-pro"
                
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(f"{instruction}\n\nQuestion: {user_input}")
                
                st.markdown("### 💡 පිළිතුර:")
                st.write(response.text)
            except Exception as e:
                st.error(f"දෝෂයක් සිදුවිය: {str(e)}")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න.")

st.markdown("---")
st.caption("© 2024 Rasanga Kalamba Arachchi")
