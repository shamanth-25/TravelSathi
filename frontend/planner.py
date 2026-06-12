import streamlit as st
from utils.i18n import t
from utils.api import get_response

st.title(f"🗺️ {t('planner_title')}")
st.write(t('planner_desc'))

st.markdown("---")

# Input parameters in two columns
col1, col2 = st.columns(2)

with col1:
    destination = st.selectbox(
        t('planner_destination'),
        options=[t('dest_hyderabad_name'), t('dest_varanasi_name'), t('dest_jaipur_name')],
        index=0
    )
    
    days = st.slider(
        t('planner_days'),
        min_value=1,
        max_value=14,
        value=3,
        step=1
    )

with col2:
    budget = st.number_input(
        t('planner_budget'),
        min_value=1000,
        max_value=500000,
        value=15000,
        step=1000
    )
    
    interests = st.text_input(
        t('planner_interests'),
        placeholder=t('planner_interests_hint')
    )

# Plan button
generate_button = st.button(t('planner_button'), type="primary", use_container_width=True)

st.markdown("---")

# Output containers
itinerary_container = st.container()
budget_container = st.container()

if generate_button:
    # Build query
    query = f"Generate {days}-day itinerary for {destination} with budget of {budget} INR. Interests: {interests}"
    
    # Retrieve language code
    lang_code = st.session_state.get("language", "en")
    provider = st.session_state.get("provider", "Gemini")
    api_key = st.session_state.get("api_key", None)
    
    # Call the frontend stub get_response
    with st.spinner("Analyzing destination and preparing itinerary..."):
        response = get_response(
            query=query,
            city=destination,
            language=lang_code,
            provider=provider,
            api_key=api_key
        )
        
    with itinerary_container:
        st.write(f"### {t('planner_itinerary_header')}")
        st.markdown(response["answer"])
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    with budget_container:
        st.write(f"### {t('planner_budget_header')}")
        
        # Display chart & metrics
        b_col1, b_col2 = st.columns([2, 3])
        
        with b_col1:
            st.write(f"#### {t('planner_est_allocation')}")
            for category, percentage in response["budget"].items():
                allocated_amount = (budget * percentage) / 100
                st.markdown(
                    f"**{category}**: {percentage}% (~₹{allocated_amount:,.2f})"
                )
                st.progress(percentage / 100)
                
        with b_col2:
            st.write(f"#### {t('planner_alloc_chart')}")
            # Present a clean bar chart representing the budget breakdown
            chart_data = {
                t('planner_category'): list(response["budget"].keys()),
                t('planner_alloc_pct'): list(response["budget"].values())
            }
            st.bar_chart(data=chart_data, x=t('planner_category'), y=t('planner_alloc_pct'), horizontal=True)

else:
    # Display initial placeholders when the page loads
    with itinerary_container:
        st.write(f"### {t('planner_itinerary_header')}")
        st.info(t('planner_placeholder_itinerary'))
        
    with budget_container:
        st.write(f"### {t('planner_budget_header')}")
        st.info(t('planner_placeholder_budget'))
