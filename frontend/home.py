import streamlit as st
import os
from utils.i18n import t

# Root assets path
assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "assets")

# Title and Tagline
st.markdown(f"# 🗺️ {t('app_title')}")
st.subheader(t('app_tagline'))
st.write(t('home_subtitle'))

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"### 📍 {t('home_featured_destinations')}")

# List of all destinations to display
destinations = [
    {
        "id": "hyderabad",
        "icon": "🕌",
        "color_bg": "rgba(255, 75, 75, 0.2)",
        "color_text": "#FF4B4B",
    },
    {
        "id": "varanasi",
        "icon": "🪔",
        "color_bg": "rgba(75, 150, 255, 0.2)",
        "color_text": "#4B96FF",
    },
    {
        "id": "jaipur",
        "icon": "🏰",
        "color_bg": "rgba(75, 255, 150, 0.2)",
        "color_text": "#4BFF96",
    },
    {
        "id": "mumbai",
        "icon": "🏙️",
        "color_bg": "rgba(255, 165, 0, 0.2)",
        "color_text": "#FFA500",
    },
    {
        "id": "kolkata",
        "icon": "🚋",
        "color_bg": "rgba(147, 112, 219, 0.2)",
        "color_text": "#9370DB",
    },
    {
        "id": "delhi",
        "icon": "🏛️",
        "color_bg": "rgba(255, 105, 180, 0.2)",
        "color_text": "#FF69B4",
    },
    {
        "id": "chennai",
        "icon": "🌴",
        "color_bg": "rgba(32, 178, 170, 0.2)",
        "color_text": "#20B2AA",
    },
    {
        "id": "ahmedabad",
        "icon": "🪁",
        "color_bg": "rgba(255, 215, 0, 0.2)",
        "color_text": "#FFD700",
    }
]

# Display cards in a 3-column layout
cols = st.columns(3)
for i, dest in enumerate(destinations):
    col = cols[i % 3]
    with col:
        img_path = os.path.join(assets_dir, f"{dest['id']}.png")
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        
        st.markdown(
            f"""
            <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 15px; margin-top: -10px; margin-bottom: 20px;">
                <h4 style="margin: 0; padding-bottom: 5px;">{dest['icon']} {t(f"dest_{dest['id']}_name", default=dest['id'].title())}</h4>
                <span style="background-color: {dest['color_bg']}; color: {dest['color_text']}; padding: 3px 8px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                    {t(f"dest_{dest['id']}_tag", default="Explore")}
                </span>
                <p style="margin-top: 10px; font-size: 0.95rem; line-height: 1.4; color: rgba(255,255,255,0.8);">
                    {t(f"dest_{dest['id']}_desc", default="Discover the beauty and culture of this amazing destination.")}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
