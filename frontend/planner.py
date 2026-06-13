import streamlit as st
import re
from utils.i18n import t
import utils.api
import importlib
importlib.reload(utils.api)
from utils.api import get_response

def parse_itinerary_into_days(text):
    if not text:
        return None, []
    # Regex to find day markers like:
    # "Day 1: Title", "Day 1 - Title", "#### Day 1", "**Day 1**", "दिन 1:", "రోజు 1:"
    # Case insensitive, matches at start of line
    pattern = r'(?:\n|^)(?:#+\s*|\*+\s*)?(?:Day|दिन|రోజు)\s*\d+.*?(?:\n|$)'
    
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    if not matches:
        return None, []
        
    intro = text[:matches[0].start()].strip()
    
    days = []
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        day_text = text[start:end].strip()
        
        # Split day_text into title and content
        lines = day_text.split('\n', 1)
        header = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        
        # Clean header (remove markdown symbols like ### or **)
        header_clean = re.sub(r'^[#*\s:-]+', '', header)
        header_clean = re.sub(r'[#*\s:-]+$', '', header_clean)
        
        days.append({
            "header": header_clean,
            "content": content
        })
        
    return intro, days

st.title(f"🗺️ {t('planner_title')}")
st.write(t('planner_desc'))

st.markdown("---")

# Input parameters in two columns
col1, col2 = st.columns(2)

with col1:
    destination = st.selectbox(
        t('planner_destination'),
        options=[
            t('dest_hyderabad_name'), 
            t('dest_varanasi_name'), 
            t('dest_jaipur_name'),
            t('dest_mumbai_name'),
            t('dest_kolkata_name'),
            t('dest_delhi_name'),
            t('dest_chennai_name'),
            t('dest_ahmedabad_name')
        ],
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
phrases_container = st.container()
budget_container = st.container()

if generate_button:
    # Build query
    query = f"Generate {days}-day itinerary for {destination} with budget of {budget} INR. Interests: {interests}"
    
    # Retrieve language code
    lang_code = st.session_state.get("language", "en")
    provider = st.session_state.get("provider", "Groq")
    api_key = st.session_state.get("api_key", None)
    
    import os
    if provider.lower() in ["groq", "openrouter", "gemini"] and not api_key and not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        st.error(f"⚠️ An API key is required to use {provider}. Please enter your {provider} API key in the Settings page.")
        st.stop()
    
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
        
        intro, days = parse_itinerary_into_days(response["answer"])
        if days:
            if intro:
                st.markdown(intro)
                st.markdown("<br>", unsafe_allow_html=True)
                
            # Create tabs for each day
            tab_labels = []
            for i, d in enumerate(days):
                day_prefix_match = re.search(r'(Day|दिन|రోజు)\s*\d+', d["header"], re.IGNORECASE)
                if day_prefix_match:
                    tab_labels.append(f"📅 {day_prefix_match.group(0)}")
                else:
                    tab_labels.append(f"📅 Day {i+1}")
                    
            tabs = st.tabs(tab_labels)
            for i, tab in enumerate(tabs):
                with tab:
                    # Show full clean header and the description inside the tab
                    st.markdown(f"#### {days[i]['header']}")
                    st.markdown(days[i]['content'])
        else:
            # Fallback if parsing fails
            st.markdown(response["answer"])
        
    with phrases_container:
        phrases_list = response.get("phrases", [])
        if phrases_list:
            st.markdown("<br>", unsafe_allow_html=True)
            st.write(f"### 🗣️ {t('phrases_header') if t('phrases_header') != 'phrases_header' else 'Useful Local Phrases'}")
            
            # Display beautiful cards for phrases
            cols_per_row = 3
            for i in range(0, len(phrases_list), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(phrases_list):
                        p = phrases_list[i + j]
                        with cols[j]:
                            if isinstance(p, dict):
                                p_phrase = p.get("phrase") or "-"
                                p_trans = p.get("translation") or p_phrase
                                p_pron = p.get("pronunciation") or "-"
                            else:
                                p_phrase = str(p)
                                p_trans = str(p)
                                p_pron = "-"
                            
                            st.markdown(
                                f"""
                                <div style="background: rgba(255, 255, 255, 0.05); border-radius: 8px; border: 1px dashed rgba(255, 255, 255, 0.15); padding: 16px; min-height: 120px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 16px;">
                                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5); font-weight: bold; text-transform: uppercase;">{t('phrases_table_phrase') if t('phrases_table_phrase') != 'phrases_table_phrase' else 'Phrase'}</div>
                                    <div style="font-size: 0.95rem; font-weight: bold; margin-bottom: 4px;">"{p_phrase}"</div>
                                    <div style="font-size: 1.10rem; color: #FF4B4B; font-weight: bold; margin-bottom: 4px;">{p_trans}</div>
                                    <div style="font-size: 0.8rem; font-style: italic; color: rgba(255,255,255,0.7);">{t('phrases_table_pronunciation') if t('phrases_table_pronunciation') != 'phrases_table_pronunciation' else 'Pronunciation'}: {p_pron}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    with budget_container:
        st.write(f"### {t('planner_budget_header')}")
        
        # Scale LLM budget to match the user's total budget exactly
        normalized_budget = {}
        for cat, val in response.get("budget", {}).items():
            try:
                normalized_budget[cat] = float(val)
            except:
                pass
                
        total_llm_amount = sum(normalized_budget.values())
        if total_llm_amount > 0:
            for cat, amt in normalized_budget.items():
                response["budget"][cat] = (amt / total_llm_amount) * budget
        else:
            response["budget"] = {"Estimated Allocation": budget}

        # Display chart & metrics
        b_col1, b_col2 = st.columns([2, 3])
        
        with b_col1:
            st.subheader("Estimated Allocation")
            for category, amount in response["budget"].items():
                percentage = (amount / budget) * 100
                st.write(
                    f"{category}: {percentage:.0f}% (₹{amount:,.2f})"
                )
                # Ensure progress bar value is between 0.0 and 1.0
                st.progress(min(max(amount / budget, 0.0), 1.0))
                
        with b_col2:
            st.write(f"#### {t('planner_alloc_chart')}")
            # Present a clean bar chart representing the budget breakdown in percentages
            chart_data = {
                t('planner_category'): list(response["budget"].keys()),
                t('planner_alloc_pct'): [(amount / budget) * 100 for amount in response["budget"].values()]
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
