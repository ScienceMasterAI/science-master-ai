import streamlit as st
import google.generativeai as genai

# API Key එක සම්බන්ධ කිරීම
GOOGLE_API_KEY = "AIzaSyCTBR6jne5xmgcGE5eMHcxpsRxby3JKqKs"
genai.configure(api_key=GOOGLE_API_KEY)

# පිටුවේ සැකසුම් (පෙනුම)
st.set_page_config(page_title="Science Master AI", page_icon="🔬", layout="centered")

# Custom CSS - ඇප් එක ලස්සන කිරීමට
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .main-title { color: #1e3a8a; text-align: center; font-weight: bold; }
    .result-box { 
        padding: 20px; 
        background-color: white; 
        border-radius: 15px; 
        border-left: 5px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #333;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar (පැති තීරුව) - මෙතන තමයි ඔයාගේ නම සහ ෆොටෝ එක තියෙන්නේ ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>නිර්මාණකරු</h2>", unsafe_allow_html=True)
    
    # පින්තූරය පෙන්වීම (Direct Link එක)
    st.image("https://i.ibb.co/v4mYpYp/rasanga.jpg", use_container_width=True)
    
    st.markdown("<h3 style='text-align: center; margin-bottom: 0;'>Rasanga Kalamba Arachchi</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Founder & Developer</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("Science Master AI යනු විෂය නිර්දේශයට අනුව විද්‍යා ගැටලු විසඳීමට සැකසූ දියුණු AI පද්ධතියකි.")

# --- ප්‍රධාන පිටුව (Main Page) ---
st.markdown("<h1 class='main-title'>🔬 Science Master AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>විභාග කේන්ද්‍රීය විද්‍යා දැනුම සහ පසුගිය ප්‍රශ්න පත්‍ර විශ්ලේෂණය</p>", unsafe_allow_html=True)
st.write("---")

user_input = st.text_area("ඔබේ විද්‍යා ගැටලුව හෝ පාඩමේ නම මෙතන ලියන්න:", 
                         placeholder="උදා: සෛලයක මයිටොකොන්ඩ්‍රියාවේ කාර්යය කුමක්ද?")

if st.button("විශ්ලේෂණය කර පිළිතුර ලබාගන්න 🚀"):
    if user_input:
        with st.spinner('දත්ත පද්ධතිය ගවේෂණය කරමින් පවතී...'):
            try:
                # වැඩ කරන ඕනෑම මොඩල් එකක් ස්වයංක්‍රීයව තෝරාගැනීම (Auto-detect model)
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model_to_use = available_models[0] if available_models else "gemini-pro"
                
                model = genai.GenerativeModel(model_to_use)
                
                # AI එකට දෙන විශේෂ උපදෙස් (Exam Focused Instructions)
                full_prompt = f"""
                You are Science Master AI, an expert science tutor created by Rasanga Kalamba Arachchi. 
                Explain the following science question deeply in Sinhala. 
                Include:
                1. Detailed explanation.
                2. Relation to the syllabus.
                3. Past paper tips and marking scheme advice.
                
                Question: {user_input}
                """
                
                response = model.generate_content(full_prompt)
                
                st.markdown("### 💡 විභාග කේන්ද්‍රීය පිළිතුර:")
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error("කණගාටුයි, පද්ධතියේ දෝෂයකි. කරුණාකර නැවත උත්සාහ කරන්න.")
    else:
        st.warning("කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න.")

st.write("---")
st.caption("© 2024 Rasanga Kalamba Arachchi | Powered by Gemini AI")
