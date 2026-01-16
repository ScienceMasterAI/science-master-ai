import streamlit as st
import google.generativeai as genai

# --- 1. API සැකසීම ---
def setup_api():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# --- 2. UI සැකසුම් ---
st.set_page_config(page_title="Science Master Pro", page_icon="🔬")

# සරල Dark Theme එකක්
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; }
    .stTextInput>div>div>input { color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 Science Master Pro AI")

# --- 3. වැඩසටහන ක්‍රියාත්මක කිරීම ---
if not setup_api():
    st.error("කරුණාකර Streamlit Secrets වල 'GOOGLE_API_KEY' ඇතුළත් කරන්න.")
    st.stop()

# Session State එක හදාගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# පරණ chat පෙන්වීම
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# අලුත් ප්‍රශ්නයක් ඇසීම
if prompt := st.chat_input("ඔබේ විද්‍යා ගැටලුව මෙතැන ලියන්න..."):
    # User message එක පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI ප්‍රතිචාරය ලබාගැනීම
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # කෙලින්ම මොඩලය කැඳවීම
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # සිංහලෙන් උත්තර දීමට බල කිරීම
            response = model.generate_content(f"Explain this clearly in Sinhala: {prompt}")
            
            if response.text:
                full_response = response.text
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("මොඩලයෙන් හිස් ප්‍රතිචාරයක් ලැබුණි.")
                
        except Exception as e:
            # ඇත්තම Error එක මොකක්ද කියලා මෙතනින් පේනවා
            st.error(f"දෝෂයක් සිදුවිය: {str(e)}")
            st.info("ඔබේ API Key එක නිවැරදිද සහ Quota ඉතිරිව තිබේදැයි පරීක්ෂා කරන්න.")

