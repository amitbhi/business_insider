"""
Frontend User Interface Entry Point.

Provides an interactive dashboard (Streamlit) for users to request
intelligence and visualize the strategic graph.
"""

import streamlit as st
import time
import requests

st.set_page_config(
    page_title="Business Insider Intelligence Engine", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠 BUSINESS_INSIDER \n#### Strategic Sovereign Intelligence Platform")

st.sidebar.header("Intelligence Request")
company_name = st.sidebar.text_input("Entity Name", "Reliance Industries Limited")
country = st.sidebar.selectbox("Jurisdiction", ["India"])

if st.sidebar.button("Run Deep Analysis"):
    st.info(f"Dispatching Multi-Agent System on {company_name}...")
    
    # 1. Trigger backend orchestrator here
    # asyncio.run(trigger_api())
    
    with st.spinner("Initializing Agents (Finance, Power, Legal, Influence)..."):
        try:
            # Hit the backend API orchestrator directly
            response = requests.post(
                "http://localhost:8000/api/v1/analyze_company/",
                json={"company_name": company_name, "country": country, "data_source": "mca"},
                timeout=30
            )
            response.raise_for_status()
            target_data = response.json()
            st.success("Target analysis compiled dynamically.")
        except Exception as e:
            st.error(f"Backend API Error: {str(e)}")
            st.stop()
            
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Strategic Intelligence Graph")
        # Placeholder for PyVis / Interactive network element
        st.markdown(f"**Entity Node:** {target_data.get('company')}")
        st.json(target_data.get("graph", {}), expanded=False)
        st.info(f"**Influence Report:** {target_data.get('influence_report')}")
        
    with col2:
        st.subheader("Critical Intelligence Profiles")
        st.warning(f"**Vulnerability:** {target_data.get('vulnerability_report')}")
        st.error(f"**Acquisition Viability:** {target_data.get('acquisition_report')}")
        st.success(f"**Executive Profile:** {target_data.get('intelligence_summary')}")

st.markdown("---")
st.text("V1 - Local DeepSeek Inference Engine | End-to-End Encrypted")
