"""Tests for the routing rules engine."""

from types import SimpleNamespace

import pytest

from ai_sdr.services.routing_service import evaluate_condition, route_lead


def _make_rule(name: str, priority: int, conditions: list, action: dict, active: bool = True):
    """Create a test RoutingRule-like object."""
    return SimpleNamespace(
        name=name, priority=priority, conditions=conditions,
        action=action, is_active=active,
    )


class TestEvaluateCondition:
    def test_equals(self):
        assert evaluate_condition(
            {"field": "company.industry", "op": "==", "value": "SaaS"},
            {"company.industry": "SaaS"},
        )

    def test_not_equals(self):
        assert evaluate_condition(
            {"field": "company.industry", "op": "!=", "value": "SaaS"},
            {"company.industry": "Healthcare"},
        )

    def test_greater_than_or_equal(self):
        assert evaluate_condition(
            {"field": "lead.score", "op": ">=", "value": 80},
            {"lead.score": 85},
        )

    def test_in_operator(self):
        assert evaluate_condition(
            {"field": "company.industry", "op": "in", "value": ["SaaS", "Fintech"]},
            {"company.industry": "Fintech"},
        )

    def test_contains(self):
        assert evaluate_condition(
            {"field": "company.name", "op": "contains", "value": "Corp"},
            {"company.name": "Acme Corp"},
        )

    def test_missing_field_returns_false(self):
        assert not evaluate_condition(
            {"field": "missing", "op": "==", "value": "anything"},
            {"other": "data"},
        )


class TestRouteLeadRules:
    def test_first_matching_rule_wins(self):
        rules = [
            _make_rule("enterprise", 0, [{"field": "lead.score", "op": ">=", "value": 80}], {"team": "enterprise"}),
            _make_rule("general", 10, [], {"team": "general"}),
        ]
        result = route_lead(rules, {"lead.score": 90})
        assert result["team"] == "enterprise"

    def test_fallback_to_default(self):
        rules = [
            _make_rule("enterprise", 0, [{"field": "lead.score", "op": ">=", "value": 80}], {"team": "enterprise"}),
            _make_rule("default", 99, [], {"team": "general"}),
        ]
        result = route_lead(rules, {"lead.score": 50})
        assert result["team"] == "general"

    def test_no_matching_rules_returns_none(self):
        rules = [
            _make_rule("enterprise", 0, [{"field": "lead.score", "op": ">=", "value": 80}], {"team": "enterprise"}),
        ]
        result = route_lead(rules, {"lead.score": 50})
        assert result is None

    def test_inactive_rules_skipped(self):
        rules = [
            _make_rule("enterprise", 0, [{"field": "lead.score", "op": ">=", "value": 80}], {"team": "enterprise"}, active=False),
            _make_rule("default", 99, [], {"team": "general"}),
        ]
        result = route_lead(rules, {"lead.score": 90})
        assert result["team"] == "general"

    def test_multiple_conditions_all_must_match(self):
        rules = [
            _make_rule(
                "enterprise_fintech",
                0,
                [
                    {"field": "lead.score", "op": ">=", "value": 80},
                    {"field": "company.industry", "op": "==", "value": "Fintech"},
                ],
                {"team": "enterprise_fintech"},
            ),
        ]
        # Both match
        assert route_lead(rules, {"lead.score": 90, "company.industry": "Fintech"})["team"] == "enterprise_fintech"
        # Only one matches
        assert route_lead(rules, {"lead.score": 90, "company.industry": "SaaS"}) is None
