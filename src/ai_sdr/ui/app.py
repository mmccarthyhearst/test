"""Streamlit dashboard for the AI SDR system."""

import os

import streamlit as st

st.set_page_config(
    page_title="AI SDR Dashboard",
    page_icon="📊",
    layout="wide",
)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.title("AI SDR Dashboard")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Leads Sourced", "—", help="Total leads found this period")
with col2:
    st.metric("Qualified", "—", help="Leads that passed ICP scoring")
with col3:
    st.metric("Meetings Booked", "—", help="Appointments scheduled")
with col4:
    st.metric("Conversion Rate", "—", help="Sourced → Meeting rate")

st.markdown("---")
st.subheader("Recent Pipeline Runs")
st.info(
    "Connect to the API to see live data. "
    f"API endpoint: {API_BASE_URL}/api/v1/pipeline/runs"
)

st.markdown("---")
st.subheader("Quick Actions")
col_a, col_b = st.columns(2)
with col_a:
    if st.button("Trigger Pipeline Run", type="primary"):
        st.warning("Pipeline trigger requires API connection. Use: POST /api/v1/pipeline/run")
with col_b:
    if st.button("View All Leads"):
        st.info("Navigate to the Leads page in the sidebar.")
