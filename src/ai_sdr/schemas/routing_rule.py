"""Routing rule schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class RuleCondition(BaseModel):
    field: str  # e.g. "company.employee_count", "company.industry", "lead.score"
    op: str  # ">=", "<=", "==", "!=", "in", "not_in", "contains"
    value: str | int | float | list


class RuleAction(BaseModel):
    team: str
    rep_id: str | None = None
    rep_name: str | None = None


class RoutingRuleCreate(BaseModel):
    name: str
    description: str | None = None
    priority: int = 0
    conditions: list[RuleCondition]
    action: RuleAction


class RoutingRuleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    priority: int | None = None
    is_active: bool | None = None
    conditions: list[RuleCondition] | None = None
    action: RuleAction | None = None


class RoutingRuleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    priority: int
    is_active: bool
    conditions: list[RuleCondition]
    action: RuleAction
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
