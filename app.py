import streamlit as st

# MUST BE FIRST Streamlit command
st.set_page_config(
    page_title="TravelSathi",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize global session states if they do not exist
if "language" not in st.session_state:
    st.session_state.language = "en"
if "provider" not in st.session_state:
    st.session_state.provider = "Offline Mock"
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Import localization utility (requires session state initialized first)
from utils.i18n import t

# Define page configuration dynamically using t() translations
home_page = st.Page("frontend/home.py", title=t("nav_home"), icon="🏠", default=True)
planner_page = st.Page("frontend/planner.py", title=t("nav_planner"), icon="🗺️")
festivals_page = st.Page("frontend/festivals.py", title=t("nav_festivals"), icon="🎉")
phrases_page = st.Page("frontend/phrases.py", title=t("nav_phrases"), icon="🗣️")
settings_page = st.Page("frontend/settings.py", title=t("nav_settings"), icon="⚙️")

# Create Navigation
pg = st.navigation([home_page, planner_page, festivals_page, phrases_page, settings_page])

# Inject Premium global styling and fonts (supports both light and dark modes via theme variables)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Premium card hover effects */
    div[data-testid="stColumn"] {
        transition: transform 0.25s ease-in-out;
    }
    
    div[data-testid="stColumn"]:hover {
        transform: translateY(-4px);
    }
    
    /* Clean custom borders for sidebar items */
    [data-testid="stSidebarNav"] {
        background-color: rgba(255, 255, 255, 0.02);
        padding-top: 15px;
        border-radius: 12px;
        margin: 10px;
    }
    
    /* Buttons custom transitions */
    div.stButton > button {
        transition: background-color 0.2s ease, transform 0.1s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Run navigation
pg.run()
