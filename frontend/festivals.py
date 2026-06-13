import streamlit as st
import os
from utils.i18n import t
import utils.api
import importlib
importlib.reload(utils.api)
from utils.api import get_response

st.title(f"🎉 {t('festivals_title')}")
st.write(t('festivals_desc'))

st.markdown("---")

# Festival selector
city_to_festivals = {
    "Hyderabad": ["Bonalu", "Bathukamma", "Makar Sankranti"],
    "Varanasi": ["Diwali", "Dev Deepawali", "Maha Shivaratri", "Holi"],
    "Jaipur": ["Teej", "Gangaur", "Kite Festival"],
    "Mumbai": ["Ganesh Chaturthi", "Gudi Padwa", "Krishna Janmashtami"],
    "Kolkata": ["Durga Puja", "Kali Puja", "Saraswati Puja"],
    "Delhi": ["Holi", "Lohri", "Dussehra", "Diwali"],
    "Chennai": ["Pongal", "Puthandu", "Thaipusam"],
    "Ahmedabad": ["Navratri", "Uttarayan", "Janmashtami"]
}

col_city, col_fest = st.columns(2)
with col_city:
    selected_city = st.selectbox(
        t('phrases_select_city', default="Select City Context"),
        options=list(city_to_festivals.keys()),
        format_func=lambda x: t(f"dest_{x.lower()}_name", default=x),
        index=0
    )

with col_fest:
    selected_festival = st.selectbox(
        t('festivals_select', default="Select a Festival"),
        options=city_to_festivals[selected_city],
        format_func=lambda x: t(f"fest_{x.lower().replace(' ', '_')}", default=x),
        index=0
    )

# Fetch data using get_response stub
lang_code = st.session_state.get("language", "en")
provider = st.session_state.get("provider", "Groq")
api_key = st.session_state.get("api_key", None)

if provider.lower() in ["groq", "openrouter"] and not api_key:
    st.error(f"⚠️ An API key is required to use {provider}. Please enter your {provider} API key in the Settings page.")
    st.stop()

query = f"festival: {selected_festival}"

with st.spinner("Retrieving cultural insights..."):
    # Determine default city context for each festival
    city_context = selected_city
        
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
    img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "assets", f"{selected_city.lower()}.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
        
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
    else:
        # Translate city name and festival name if they exist in translation dictionaries
        translated_city = t(f"dest_{selected_city.lower()}_name", default=selected_city)
        translated_festival = t(f"fest_{selected_festival.lower().replace(' ', '_')}", default=selected_festival)
        
        etiquette_template = t('fest_default_etiquette')
        formatted_etiquette = etiquette_template.replace("{festival}", translated_festival).replace("{city}", translated_city)
        st.markdown(formatted_etiquette)
