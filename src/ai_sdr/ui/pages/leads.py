"""Leads management page."""

import streamlit as st

st.title("Leads")
st.markdown("Browse, filter, and manage leads in the pipeline.")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    status_filter = st.selectbox(
        "Status",
        ["All", "New", "Qualified", "Routed", "Contacted", "Meeting Booked", "Disqualified"],
    )
with col2:
    tier_filter = st.selectbox("Tier", ["All", "Hot", "Warm", "Cold"])
with col3:
    team_filter = st.text_input("Assigned Team", placeholder="e.g., Enterprise")

st.markdown("---")
st.info("Connect to the API to see live lead data. Endpoint: GET /api/v1/leads")
