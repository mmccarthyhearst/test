"""Shared test fixtures."""

import pytest


@pytest.fixture
def sample_icp_criteria() -> dict:
    """Sample ICP criteria for testing."""
    return {
        "name": "Enterprise SaaS",
        "target_industries": ["Technology", "SaaS", "Software"],
        "min_employee_count": 50,
        "max_employee_count": 5000,
        "target_titles": ["VP of Sales", "CRO", "Head of Revenue"],
        "target_seniority": ["C-Suite", "VP", "Director"],
        "target_geography": ["US", "Canada"],
        "required_tech_stack": ["Salesforce", "Python"],
    }


@pytest.fixture
def sample_scoring_weights() -> dict:
    """Sample scoring weights."""
    return {
        "industry": 25,
        "company_size": 20,
        "seniority": 20,
        "title": 15,
        "geography": 10,
        "tech_stack": 10,
    }
