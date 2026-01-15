import streamlit as st
import google.generativeai as genai

# API Key
GOOGLE_API_KEY = "AIzaSyCTBR6jne5xmgcGE5eMHcxpsRxby3JKqKs"
genai.configure(api_key=GOOGLE_API_KEY)

# පිටුවේ පෙනුම සහ Design එක සැකසීම
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

# Custom CSS - ඇප් එක ලස්සන කිරීමට
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f9;
    }
    .main-title {
        color: #1e3a8a;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .result-box {
        padding: 20px;
        background-color: white;
        border-radius: 15px;
        border-left: 5px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# AI එකට දෙන පට්ටම උපදෙස් මාලාව (Past Paper & Syllabus Knowledge)
instruction = """
You are 'Science Master AI', an expert science tutor created by Rasanga Kalamba Arachchi.
Your specialty is the Sri Lankan O/L and A/L Science syllabus.
When a user asks a question:
1. Provide a detailed scientific explanation in Sinhala.
2. Relate it to the official syllabus.
3. Mention how this appears in Past Papers and give tips to get full marks.
4. Use bullet points and LaTeX for formulas like $E=mc^2$.
"""

# Sidebar (පැති තීරුව) - Rasanga ගේ විස්තර සහ පින්තූරය
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>නිර්මාණකරු</h2>", unsafe_allow_html=True)
    
    # ඔයාගේ පින්තූරය ලින්ක් එකක් ලෙස
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", caption="Rasanga Kalamba Arachchi", use_container_width=True)
    
    st.markdown("<h3 style='text-align: center;'>Rasanga Kalamba Arachchi</h3>", unsafe_allow_html=True)
    st.info("විද්‍යා විෂය නිර්දේශය සහ පසුගිය විභාග ප්‍රශ්න පිළිබඳ විශේෂ දැනුමක් සහිත AI පද්ධතියකි.")
    st.write("ඕනෑම විද්‍යා ගැටලුවකට නිවැරදි පිළිතුරු ලබා දීමට මෙම පද්ධතිය මා විසින් නිර්මාණය කරන ලදී.")

# ප්‍රධාන පිටුව
st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>විභාග කේන්ද්‍රීය විද්‍යා දැනුම ලබාගන්න</p>", unsafe_allow_html=True)
st.write("---")

user_input = st.text_area("ඔබේ විද්‍යා ගැටලුව සිංහලෙන් මෙතන ලියන්න:", placeholder="උදා: නියුටන්ගේ දෙවන නියමය පැහැදිලි කරන්න.")

if st.button("විශ්ලේෂණය කර පිළිතුර ලබාගන්න 🚀"):
    if user_input:
        with st.spinner('දත්ත පද්ධතිය පරීක්ෂා කරමින් පවතී...'):
            try:
                # දියුණු දැනුම සහිත Model එක
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    system_instruction=instruction
                )
                
                response = model.generate_content(user_input)
                
                st.markdown("### 💡 විභාග කේන්ද්‍රීය විශ්ලේෂණය:")
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error("කණගාටුයි, නැවත උත්සාහ කරන්න.")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න.")

st.write("---")
st.caption("© 2024 Rasanga Kalamba Arachchi | All Rights Reserved")
