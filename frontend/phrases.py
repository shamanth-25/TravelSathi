import streamlit as st
import pandas as pd
from utils.i18n import t
import utils.api
import importlib
importlib.reload(utils.api)
from utils.api import get_response

st.title(f"🗣️ {t('phrases_title')}")
st.write(t('phrases_desc'))

st.markdown("---")

# Select city context
city_option = st.selectbox(
    t('phrases_select_city'),
    options=[
        t('dest_hyderabad_name'), 
        t('dest_varanasi_name'), 
        t('dest_jaipur_name'),
        t('dest_mumbai_name'),
        t('dest_kolkata_name'),
        t('dest_delhi_name'),
        t('dest_chennai_name'),
        t('dest_ahmedabad_name'),
        "General"
    ],
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
    # Render beautiful flashcards for each phrase for premium touch
    cols_per_row = 3
    for i in range(0, len(phrases_list), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(phrases_list):
                p = phrases_list[i + j]
                with cols[j]:
                    if isinstance(p, str):
                        # Attempt to split if LLM provided a string like "नमस्ते (Namaste) - Hello"
                        parts = p.split(" - ")
                        if len(parts) == 2:
                            p_phrase = parts[1].strip()
                            trans_part = parts[0].strip()
                            p_pron = "N/A"
                            
                            # Try to extract pronunciation from parentheses
                            if "(" in trans_part and ")" in trans_part:
                                sub_parts = trans_part.split("(", 1)
                                trans_clean = sub_parts[0].strip()
                                pron_clean = sub_parts[1].split(")")[0].strip()
                                p_trans = trans_clean
                                p_pron = pron_clean
                            else:
                                p_trans = trans_part
                        else:
                            p_phrase = p
                            p_trans = p
                            p_pron = "-"
                    elif isinstance(p, dict):
                        # Check standard keys first
                        phrase_val = p.get("phrase")
                        trans_val = p.get("translation")
                        pron_val = p.get("pronunciation")
                        
                        # If standard keys failed, perhaps the LLM translated the keys
                        if not phrase_val and not trans_val and not pron_val:
                            vals = list(p.values())
                            p_phrase = vals[0] if len(vals) > 0 else "-"
                            p_trans = vals[1] if len(vals) > 1 else p_phrase
                            p_pron = vals[2] if len(vals) > 2 else "-"
                        else:
                            p_phrase = phrase_val or "-"
                            p_trans = trans_val or p_phrase
                            p_pron = pron_val or "-"
                    else:
                        p_phrase = "-"
                        p_trans = "-"
                        p_pron = "-"
                        
                    st.markdown(
                        f"""
                        <div style="background: rgba(255, 255, 255, 0.05); border-radius: 8px; border: 1px dashed rgba(255, 255, 255, 0.15); padding: 16px; min-height: 160px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 16px;">
                            <div style="font-size: 0.85rem; color: rgba(255,255,255,0.5); font-weight: bold; text-transform: uppercase;">{t('phrases_table_phrase')}</div>
                            <div style="font-size: 1rem; font-weight: bold; margin-bottom: 8px;">"{p_phrase}"</div>
                            <div style="font-size: 1.2rem; color: #FF4B4B; font-weight: bold; margin-bottom: 8px;">{p_trans}</div>
                            <div style="font-size: 0.85rem; font-style: italic; color: rgba(255,255,255,0.7);">{t('phrases_table_pronunciation')}: {p_pron}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
else:
    st.warning("No local phrases found for this context.")

# Custom phrase translator
st.write("---")
title_text = t('phrases_translate_custom')
st.write(f"### 💬 {'Translate Custom Phrase' if title_text == 'phrases_translate_custom' else title_text}")

input_text = t('phrases_enter_custom')
custom_phrase = st.text_input("Enter a phrase to translate:" if input_text == 'phrases_enter_custom' else input_text, placeholder="e.g. How much does this cost?")

btn_text = t('phrases_translate_button')
if st.button("Translate" if btn_text == 'phrases_translate_button' else btn_text, type="primary"):
    if custom_phrase.strip():
        translate_query = f"TRANSLATE_PHRASE: {custom_phrase}"
        with st.spinner("Translating..."):
            trans_response = get_response(
                query=translate_query,
                city=city_option,
                language=lang_code,
                provider=provider,
                api_key=api_key
            )
            
            custom_phrases_list = trans_response.get("phrases", [])
            if custom_phrases_list:
                for p in custom_phrases_list:
                    phrase_label = p.get('phrase', custom_phrase)
                    st.markdown(
                        f"""
                        <div style="background: rgba(255, 255, 255, 0.05); border-radius: 8px; border: 1px dashed rgba(75, 255, 75, 0.5); padding: 16px; margin-top: 10px;">
                            <div style="font-size: 0.85rem; color: rgba(255,255,255,0.5); font-weight: bold; text-transform: uppercase;">Translation for "{phrase_label}"</div>
                            <div style="font-size: 1.5rem; color: #4BFF4B; font-weight: bold; margin: 10px 0;">{p.get('translation', 'N/A')}</div>
                            <div style="font-size: 1rem; font-style: italic; color: rgba(255,255,255,0.7);">Pronunciation: {p.get('pronunciation', 'N/A')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.error("Failed to translate the phrase. Please try again.")
    else:
        st.warning("Please enter a phrase first.")
