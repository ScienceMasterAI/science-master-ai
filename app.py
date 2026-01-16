import google.generativeai as genai

# --- API Key එක ඇතුළත් කිරීම ---
# ආරක්ෂාව සඳහා මෙය අන් අයට පෙනෙන්නට නොතැබීමට වගබලා ගන්න.
GOOGLE_API_KEY = "AIzaSyAzqgn6qnQHF28ck_a1uGD6CDSVqZEU28A"
genai.configure(api_key=GOOGLE_API_KEY)

# පිටුවේ සැකසුම් (Page Config)
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

# පෙනුම ලස්සන කිරීමට CSS
st.markdown("""
    <style>
    .main-title { color: #1e3a8a; text-align: center; font-weight: bold; font-size: 35px; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1e3a8a; color: white; height: 50px; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# පැති තීරුව (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>නිර්මාණකරු</h2>", unsafe_allow_html=True)
    try:
        st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    except:
        st.info("පින්තූරය පූරණය කළ නොහැක.")
    st.markdown("<p style='text-align: center; font-weight: bold;'>Rasanga Kalamba Arachchi</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("මෙම AI පද්ධතිය මගින් ඕනෑම විද්‍යා ප්‍රශ්නයක් විෂය නිර්දේශයට අනුව පැහැදිලි කර දේ.")

# ප්‍රධාන කොටස
st.markdown("<div class='main-title'>🔬 Science Master AI</div>", unsafe_allow_html=True)
st.write("---")

user_input = st.text_area("ඔබේ විද්‍යා ප්‍රශ්නය සිංහලෙන් ඇතුළත් කරන්න:", height=150, placeholder="උදා: ආලෝකයේ වර්තනය යනු කුමක්ද?")

if st.button("පිළිතුර ලබාගන්න ✨"):
    if user_input:
        with st.spinner('පිළිතුර සකස් කරමින් පවතී...'):
            try:
                # නවතම 1.5-flash මාදිලිය භාවිතා කරමු
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Instruction එකක් සමඟ පණිවිඩය යැවීම
                prompt = f"You are a science teacher. Explain the following question in detail using Sinhala language, including key points for exams: {user_input}"
                response = model.generate_content(prompt)
                
                st.markdown("### 💡 පිළිතුර:")
                st.info(response.text)
                
            except Exception as e:
                # වැරැද්දක් ආවොත් එය පෙන්වීමට
                if "403" in str(e):
                    st.error("API Key එක නැවතත් අවලංගු වී ඇත. කරුණාකර අලුත් Key එකක් ලබා ගන්න.")
                else:
                    st.error(f"දෝෂයක් සිදුවිය: {str(e)}")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න.")

st.markdown("---")
st.caption("© 2026 Science Master AI | Created by Rasanga")
