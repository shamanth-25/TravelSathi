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

# Display cards in a 3-column layout
col1, col2, col3 = st.columns(3)

with col1:
    img_path = os.path.join(assets_dir, "hyderabad.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    
    st.markdown(
        f"""
        <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 15px; margin-top: -10px;">
            <h4 style="margin: 0; padding-bottom: 5px;">🕌 {t('dest_hyderabad_name')}</h4>
            <span style="background-color: rgba(255, 75, 75, 0.2); color: #FF4B4B; padding: 3px 8px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                {t('dest_hyderabad_tag')}
            </span>
            <p style="margin-top: 10px; font-size: 0.95rem; line-height: 1.4; color: rgba(255,255,255,0.8);">
                {t('dest_hyderabad_desc')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    img_path = os.path.join(assets_dir, "varanasi.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
        
    st.markdown(
        f"""
        <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 15px; margin-top: -10px;">
            <h4 style="margin: 0; padding-bottom: 5px;">🪔 {t('dest_varanasi_name')}</h4>
            <span style="background-color: rgba(75, 150, 255, 0.2); color: #4B96FF; padding: 3px 8px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                {t('dest_varanasi_tag')}
            </span>
            <p style="margin-top: 10px; font-size: 0.95rem; line-height: 1.4; color: rgba(255,255,255,0.8);">
                {t('dest_varanasi_desc')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    img_path = os.path.join(assets_dir, "jaipur.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
        
    st.markdown(
        f"""
        <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 15px; margin-top: -10px;">
            <h4 style="margin: 0; padding-bottom: 5px;">🏰 {t('dest_jaipur_name')}</h4>
            <span style="background-color: rgba(75, 255, 150, 0.2); color: #4BFF96; padding: 3px 8px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                {t('dest_jaipur_tag')}
            </span>
            <p style="margin-top: 10px; font-size: 0.95rem; line-height: 1.4; color: rgba(255,255,255,0.8);">
                {t('dest_jaipur_desc')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
