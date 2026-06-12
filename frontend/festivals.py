import streamlit as st
from utils.i18n import t
from utils.api import get_response

st.title(f"🎉 {t('festivals_title')}")
st.write(t('festivals_desc'))

st.markdown("---")

# Festival selector
fest_map = {
    t('fest_bonalu'): "Bonalu",
    t('fest_diwali'): "Diwali",
    t('fest_teej'): "Teej"
}

selected_label = st.selectbox(
    t('festivals_select'),
    options=[t('fest_bonalu'), t('fest_diwali'), t('fest_teej')],
    index=0
)
selected_festival = fest_map.get(selected_label, "Bonalu")

# Fetch data using get_response stub
lang_code = st.session_state.get("language", "en")
provider = st.session_state.get("provider", "Gemini")
api_key = st.session_state.get("api_key", None)

query = f"festival: {selected_festival}"

with st.spinner("Retrieving cultural insights..."):
    # Determine default city context for each festival
    city_context = "India"
    if selected_festival == "Bonalu":
        city_context = "Hyderabad"
    elif selected_festival == "Diwali":
        city_context = "Varanasi"
    elif selected_festival == "Teej":
        city_context = "Jaipur"
        
    response = get_response(
        query=query,
        city=city_context,
        language=lang_code,
        provider=provider,
        api_key=api_key
    )

# Sub-content layout
col1, col2 = st.columns(2)

with col1:
    st.write(f"### ℹ️ {t('festivals_explanation_header')}")
    st.markdown(response["answer"])

with col2:
    st.write(f"### 💡 {t('festivals_etiquette_header')}")
    
    # Custom etiquette tips based on selection
    if selected_festival == "Bonalu":
        st.markdown(t('fest_bonalu_etiquette'))
    elif selected_festival == "Diwali":
        st.markdown(t('fest_diwali_etiquette'))
    elif selected_festival == "Teej":
        st.markdown(t('fest_teej_etiquette'))
