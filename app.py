import streamlit as st
import google.generativeai as genai

# --- API එක සැකසීම ---
def setup_api():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        # මෙතනදී අලුත්ම API පද්ධතිය භාවිතා කරයි
        genai.configure(api_key=api_key)
        return True
    return False

st.set_page_config(page_title="Science Master Pro", page_icon="🔬")

st.title("🔬 Science Master Pro AI")

if not setup_api():
    st.error("කරුණාකර Secrets වල API Key එක ඇතුළත් කරන්න.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("ප්‍රශ්නය මෙතැන ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # 404 Error එක නැති කිරීමට 'models/' කෑල්ල අතහැර 'gemini-1.5-flash' පමණක් භාවිතා කිරීම
            # සමහර විට models/gemini-pro ලෙස උත්සාහ කරන්න
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(f"Explain in simple Sinhala: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
        except Exception as e:
            # තවමත් error එක එනවා නම් gemini-pro උත්සාහ කරයි
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"Explain in simple Sinhala: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error(f"නැවතත් දෝෂයක්: {str(e)}")
                st.info("ඔබේ Google AI Studio එකේ 'Gemini API' එක activate වී ඇත්දැයි බලන්න.")
