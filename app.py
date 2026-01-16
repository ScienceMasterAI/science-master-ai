import streamlit as st
import google.generativeai as genai

# API එක සෙට් කිරීම
def setup_api():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# වැඩ කරන මොඩල් එකක් සොයා ගැනීම (404 Error එක නැති කරයි)
def get_model():
    # උත්සාහ කර බලන මොඩල් ලැයිස්තුව
    test_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for m_name in test_models:
        try:
            model = genai.GenerativeModel(m_name)
            # මොඩල් එක වැඩද කියා පොඩි ටෙස්ට් එකක් කරයි
            model.generate_content("hi", generation_config={"max_output_tokens": 1})
            return model
        except:
            continue
    return None

st.set_page_config(page_title="Science AI", page_icon="🔬")
st.title("🔬 Science Master AI")

if setup_api():
    model = get_model()
    
    if model:
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
                    # සිංහලෙන් පිළිතුරු දීමට බල කිරීම
                    response = model.generate_content(f"Explain clearly in Sinhala: {prompt}")
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"දෝෂයක්: {e}")
    else:
        st.error("ඔබේ API Key එකට ගැලපෙන මොඩලයක් හමු නොවීය. කරුණාකර අලුත් API Key එකක් උත්සාහ කරන්න.")
else:
    st.warning("Secrets වල API Key එක ඇතුළත් කර නැත.")
