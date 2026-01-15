import streamlit as st
import google.generativeai as genai

# API Key
GOOGLE_API_KEY = "AIzaSyCTBR6jne5xmgcGE5eMHcxpsRxby3JKqKs"
genai.configure(api_key=GOOGLE_API_KEY)

# පිටුවේ පෙනුම
st.set_page_config(page_title="Science Master AI", page_icon="🔬")

# Sidebar එකේ ඔයාගේ විස්තර සහ පින්තූරය
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>නිර්මාණකරු</h2>", unsafe_allow_html=True)
    
    # ඔයාගේ පින්තූරය (මම මේක ලින්ක් එකක් විදිහට දැම්මා)
    user_image = "https://raw.githubusercontent.com/ScienceMasterAI/science-master-ai/main/me.jpg" 
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", caption="Rasanga Kalamba Arachchi", use_container_width=True)
    
    st.markdown("<h3 style='text-align: center;'>Rasanga Kalamba Arachchi</h3>", unsafe_allow_html=True)
    st.info("Science Master AI හි නිල නිර්මාණකරු.")
    st.write("ඕනෑම විද්‍යා ගැටලුවකට නිවැරදි පිළිතුරු ලබා දීමට මෙම AI පද්ධතිය සැකසූ වගයි.")

# ප්‍රධාන පිටුව
st.title("🔬 Science Master AI")
st.markdown("---")
st.write("ඕනෑම විද්‍යා ගැටලුවක් සිංහලෙන් අහන්න!")

user_input = st.text_input("ඔබේ ප්‍රශ්නය මෙතන ලියන්න:", placeholder="උදා: සූර්යයා සෑදී ඇත්තේ කුමන වායූන්ගෙන්ද?")

if st.button("පිළිතුර ලබාගන්න"):
    if user_input:
        with st.spinner('පිළිතුර සකස් කරමින්...'):
            try:
                # වැඩ කරන මොඩල් එකක් තෝරාගැනීම
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Answer in clear Sinhala: {user_input}")
                st.success("පිළිතුර සූදානම්!")
                st.write(response.text)
            except:
                st.error("පද්ධතියේ පොඩි දෝෂයක්. කරුණාකර නැවත උත්සාහ කරන්න.")
    else:
        st.warning("ප්‍රශ්නයක් ලියන්න.")

st.markdown("---")
st.caption("Developed by Rasanga Kalamba Arachchi")
