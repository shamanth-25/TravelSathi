import streamlit as st
import json
import os

def load_translations(lang):
    """
    Load JSON file for target language from 'translations/' directory.
    If the file is not found, fallback to English.
    """
    # Build path relative to the root directory
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "translations", f"{lang}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # Fallback to English
        fallback_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "translations", "en.json")
        try:
            with open(fallback_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

def t(key):
    """
    Retrieve translated string based on the language saved in st.session_state.
    Uses cached translation dictionary in st.session_state to avoid disk I/O.
    """
    # Normalize language string to standard codes 'en', 'te', 'hi'
    lang_mapping = {
        "English": "en",
        "Telugu": "te",
        "Hindi": "hi",
        "en": "en",
        "te": "te",
        "hi": "hi"
    }
    raw_lang = st.session_state.get("language", "en")
    lang = lang_mapping.get(raw_lang, "en")
    
    cache_key = f"trans_dict_{lang}"
    if cache_key not in st.session_state:
        st.session_state[cache_key] = load_translations(lang)
        
    trans_dict = st.session_state[cache_key]
    return trans_dict.get(key, key)
