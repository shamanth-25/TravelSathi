import streamlit as st
from utils.i18n import t

st.title(f"⚙️ {t('settings_title')}")
st.write(t('settings_desc'))

st.markdown("---")

# Code maps
lang_display_to_code = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi"
}
lang_code_to_display = {
    "en": "English",
    "te": "Telugu",
    "hi": "Hindi"
}

# Load current session configurations
current_lang_code = st.session_state.get("language", "en")
current_lang_display = lang_code_to_display.get(current_lang_code, "English")
current_provider = st.session_state.get("provider", "Gemini")
current_api_key = st.session_state.get("api_key", "")
current_ollama_url = st.session_state.get("ollama_url", "http://localhost:11434")

# 1. Language selector
selected_lang_display = st.selectbox(
    t('settings_language'),
    options=["English", "Telugu", "Hindi"],
    index=["English", "Telugu", "Hindi"].index(current_lang_display)
)

# 2. AI Provider selector
provider_options = ["Gemini", "Ollama", "Groq", "OpenRouter", "Offline Mock"]
if current_provider not in provider_options:
    current_provider = "Offline Mock"

selected_provider = st.selectbox(
    t('settings_provider'),
    options=provider_options,
    index=provider_options.index(current_provider)
)

# 3. API Key password input (not needed for Ollama or Offline Mock, but keep for simplicity)
selected_api_key = st.text_input(
    t('settings_api_key'),
    value=current_api_key,
    type="password"
)

# 4. Ollama Endpoint URL input (conditional on Ollama selection)
selected_ollama_url = current_ollama_url
if selected_provider == "Ollama":
    selected_ollama_url = st.text_input(
        "Ollama Endpoint URL",
        value=current_ollama_url,
        help="Use http://localhost:11434 for local machine, or your public Ngrok tunnel URL (e.g. https://xxx.ngrok.app) for cloud deployment."
    )

st.markdown("<br>", unsafe_allow_html=True)

# 5. Save button
if st.button(t('settings_save'), type="primary", use_container_width=True):
    new_lang_code = lang_display_to_code.get(selected_lang_display, "en")
    
    # Save back to session state
    st.session_state.language = new_lang_code
    st.session_state.provider = selected_provider
    st.session_state.api_key = selected_api_key
    st.session_state.ollama_url = selected_ollama_url
    
    # Invalidate translations cache to trigger reload of target language
    for key in list(st.session_state.keys()):
        if key.startswith("trans_dict_"):
            del st.session_state[key]
            
    # Success message
    st.toast(t('settings_saved_success'), icon="✅")
    st.success(t('settings_saved_success'))
    
    # Force full rerun of the page to apply new translations
    st.rerun()
