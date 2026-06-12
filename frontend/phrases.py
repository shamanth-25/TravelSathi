import streamlit as st
import pandas as pd
from utils.i18n import t
from utils.api import get_response

st.title(f"🗣️ {t('phrases_title')}")
st.write(t('phrases_desc'))

st.markdown("---")

# Select city context
city_option = st.selectbox(
    t('phrases_select_city'),
    options=[t('dest_hyderabad_name'), t('dest_varanasi_name'), t('dest_jaipur_name'), "General"],
    index=0
)

# Fetch phrases from get_response stub
lang_code = st.session_state.get("language", "en")
provider = st.session_state.get("provider", "Gemini")
api_key = st.session_state.get("api_key", None)

query = f"Get useful phrases for {city_option}"

with st.spinner("Loading phrases..."):
    response = get_response(
        query=query,
        city=city_option,
        language=lang_code,
        provider=provider,
        api_key=api_key
    )

st.write(f"### 📋 {t('phrases_header')}")

# Display phrases in a structured format
phrases_list = response.get("phrases", [])

if phrases_list:
    # Convert list of dicts to a pandas DataFrame for a nice UI table display
    df_data = []
    for p in phrases_list:
        df_data.append({
            t('phrases_table_phrase'): p["phrase"],
            t('phrases_table_translation'): p["translation"],
            t('phrases_table_pronunciation'): p["pronunciation"]
        })
    
    df = pd.DataFrame(df_data)
    
    # Render table beautifully
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Also render beautiful flashcards for each phrase for premium touch
    st.write("---")
    st.write("#### 💡 Phrase Flashcards")
    
    f_cols = st.columns(len(phrases_list))
    for i, p in enumerate(phrases_list):
        with f_cols[i % len(f_cols)]:
            st.markdown(
                f"""
                <div style="background: rgba(255, 255, 255, 0.05); border-radius: 8px; border: 1px dashed rgba(255, 255, 255, 0.15); padding: 12px; height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="font-size: 0.85rem; color: rgba(255,255,255,0.5); font-weight: bold; text-transform: uppercase;">{t('phrases_table_phrase')}</div>
                    <div style="font-size: 1rem; font-weight: bold; margin-bottom: 5px;">"{p['phrase']}"</div>
                    <div style="font-size: 1.1rem; color: #FF4B4B; font-weight: bold;">{p['translation']}</div>
                    <div style="font-size: 0.85rem; font-style: italic; color: rgba(255,255,255,0.7);">{t('phrases_table_pronunciation')}: {p['pronunciation']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.warning("No local phrases found for this context.")
