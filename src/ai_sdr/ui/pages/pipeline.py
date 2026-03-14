"""Pipeline management page."""

import streamlit as st

st.title("Pipeline Runs")
st.markdown("Trigger new runs and monitor execution history.")

st.subheader("Trigger New Run")
with st.form("trigger_run"):
    icp_id = st.text_input("ICP ID (optional)", placeholder="UUID of the ICP to use")
    max_leads = st.number_input("Max Leads", min_value=1, max_value=100, value=10)
    dry_run = st.checkbox("Dry Run (no emails sent)")
    submitted = st.form_submit_button("Start Pipeline Run", type="primary")
    if submitted:
        st.warning("Pipeline trigger requires API connection. Use: POST /api/v1/pipeline/run")

st.markdown("---")
st.subheader("Run History")
st.info("Connect to the API to see pipeline run history. Endpoint: GET /api/v1/pipeline/runs")
