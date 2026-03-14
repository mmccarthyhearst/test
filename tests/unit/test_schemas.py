"""Tests for Pydantic schemas — especially the agent contract schemas."""

import pytest
from pydantic import ValidationError

from ai_sdr.schemas.agent import (
    BuyingSignal,
    LeadCandidate,
    OutreachResult,
    QualifiedLead,
    RoutedLead,
)


class TestLeadCandidate:
    def test_valid_candidate(self):
        c = LeadCandidate(
            company_name="Acme",
            company_domain="acme.com",
            contact_first_name="Jane",
            contact_last_name="Smith",
            contact_email="jane@acme.com",
        )
        assert c.company_name == "Acme"
        assert c.source == "web_scrape"

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            LeadCandidate(company_name="Acme")


class TestQualifiedLead:
    def test_valid_qualified_lead(self):
        candidate = LeadCandidate(
            company_name="Acme",
            company_domain="acme.com",
            contact_first_name="Jane",
            contact_last_name="Smith",
            contact_email="jane@acme.com",
        )
        ql = QualifiedLead(
            candidate=candidate,
            score=85,
            tier="hot",
            qualification_reasoning="Strong ICP fit with active hiring.",
        )
        assert ql.score == 85
        assert ql.tier == "hot"
        assert ql.meets_icp is True


class TestRoutedLead:
    def test_valid_routed_lead(self):
        candidate = LeadCandidate(
            company_name="Acme",
            company_domain="acme.com",
            contact_first_name="Jane",
            contact_last_name="Smith",
            contact_email="jane@acme.com",
        )
        ql = QualifiedLead(
            candidate=candidate,
            score=85,
            tier="hot",
            qualification_reasoning="Strong fit.",
        )
        rl = RoutedLead(
            qualified_lead=ql,
            assigned_team="enterprise",
            routing_reasoning="Score >= 80 matched enterprise rule.",
        )
        assert rl.assigned_team == "enterprise"


class TestOutreachResult:
    def test_valid_outreach_result(self):
        candidate = LeadCandidate(
            company_name="Acme",
            company_domain="acme.com",
            contact_first_name="Jane",
            contact_last_name="Smith",
            contact_email="jane@acme.com",
        )
        ql = QualifiedLead(
            candidate=candidate,
            score=85,
            tier="hot",
            qualification_reasoning="Good fit.",
        )
        rl = RoutedLead(
            qualified_lead=ql,
            assigned_team="enterprise",
            routing_reasoning="Rule match.",
        )
        result = OutreachResult(
            routed_lead=rl,
            email_sent=True,
            email_subject="Quick question about Acme's growth",
            meeting_booked=False,
        )
        assert result.email_sent is True
        assert result.meeting_booked is False
