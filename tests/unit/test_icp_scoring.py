"""Tests for ICP scoring logic."""

from types import SimpleNamespace

import pytest

from ai_sdr.schemas.agent import LeadCandidate
from ai_sdr.services.icp_service import score_lead_against_icp


def _make_icp(**kwargs):
    """Create a test ICP-like object."""
    defaults = {
        "target_industries": ["Technology", "SaaS"],
        "min_employee_count": 50,
        "max_employee_count": 5000,
        "target_titles": ["VP of Sales", "CRO"],
        "target_seniority": ["C-Suite", "VP"],
        "target_geography": ["US"],
        "required_tech_stack": ["Salesforce", "Python"],
        "scoring_weights": {
            "industry": 20,
            "company_size": 20,
            "seniority": 20,
            "title": 15,
            "geography": 10,
            "tech_stack": 15,
        },
        "custom_criteria": None,
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _make_candidate(**kwargs) -> LeadCandidate:
    """Create a test LeadCandidate."""
    defaults = {
        "company_name": "Acme Corp",
        "company_domain": "acme.com",
        "industry": "Technology",
        "employee_count_range": "100-500",
        "hq_location": "San Francisco, US",
        "tech_stack": ["Salesforce", "Python", "AWS"],
        "contact_first_name": "Jane",
        "contact_last_name": "Smith",
        "contact_email": "jane@acme.com",
        "contact_title": "VP of Sales",
        "contact_seniority": "VP",
    }
    defaults.update(kwargs)
    return LeadCandidate(**defaults)


class TestICPScoring:
    def test_perfect_match_scores_high(self):
        icp = _make_icp()
        candidate = _make_candidate()
        score = score_lead_against_icp(candidate, icp)
        assert score >= 80, f"Perfect match should score 80+, got {score}"

    def test_no_match_scores_low(self):
        icp = _make_icp()
        candidate = _make_candidate(
            industry="Healthcare",
            employee_count_range="1-10",
            hq_location="Tokyo, Japan",
            tech_stack=["Ruby", "Heroku"],
            contact_title="Intern",
            contact_seniority="IC",
        )
        score = score_lead_against_icp(candidate, icp)
        assert score <= 20, f"No match should score 20 or less, got {score}"

    def test_partial_match(self):
        icp = _make_icp()
        candidate = _make_candidate(
            industry="Technology",  # Match
            employee_count_range="100-500",  # Match
            contact_title="Software Engineer",  # No match
            contact_seniority="IC",  # No match
            tech_stack=["Salesforce"],  # Partial match
        )
        score = score_lead_against_icp(candidate, icp)
        assert 30 <= score <= 70, f"Partial match should be 30-70, got {score}"

    def test_missing_data_doesnt_crash(self):
        icp = _make_icp()
        candidate = _make_candidate(
            industry=None,
            employee_count_range=None,
            hq_location=None,
            tech_stack=None,
            contact_title=None,
            contact_seniority=None,
        )
        score = score_lead_against_icp(candidate, icp)
        assert 0 <= score <= 100

    def test_empty_icp_returns_default(self):
        icp = _make_icp(
            target_industries=None,
            min_employee_count=None,
            max_employee_count=None,
            target_titles=None,
            target_seniority=None,
            target_geography=None,
            required_tech_stack=None,
            scoring_weights=None,
        )
        candidate = _make_candidate()
        score = score_lead_against_icp(candidate, icp)
        assert score == 50, "Empty ICP should return default score of 50"
