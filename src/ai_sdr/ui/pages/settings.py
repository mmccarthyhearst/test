"""Settings page — manage ICPs and routing rules."""

import streamlit as st

st.title("Settings")

tab1, tab2 = st.tabs(["ICP Definitions", "Routing Rules"])

with tab1:
    st.subheader("Ideal Customer Profiles")
    st.info("Manage ICP definitions via the API: GET/POST /api/v1/icp")

    with st.expander("Create New ICP"):
        with st.form("create_icp"):
            name = st.text_input("ICP Name", placeholder="e.g., Enterprise SaaS")
            industries = st.text_input("Target Industries (comma-separated)")
            min_emp = st.number_input("Min Employees", min_value=0, value=50)
            max_emp = st.number_input("Max Employees", min_value=0, value=5000)
            titles = st.text_input("Target Titles (comma-separated)", placeholder="VP of Sales, CRO")
            geography = st.text_input("Geography (comma-separated)", placeholder="US, EMEA")
            submitted = st.form_submit_button("Create ICP")
            if submitted:
                st.success(f"ICP '{name}' would be created. Connect API to enable.")

with tab2:
    st.subheader("Lead Routing Rules")
    st.info("Manage routing rules via the API: GET/POST /api/v1/routing-rules")
    st.markdown(
        """
        Rules are evaluated in **priority order** (lower number = higher priority).
        The first matching rule wins. Add a catch-all rule with empty conditions as fallback.
        """
    )
