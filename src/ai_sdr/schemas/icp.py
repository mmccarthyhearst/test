"""ICP (Ideal Customer Profile) schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class ICPBase(BaseModel):
    name: str
    description: str | None = None
    target_industries: list[str] | None = None
    min_employee_count: int | None = None
    max_employee_count: int | None = None
    min_revenue: str | None = None
    max_revenue: str | None = None
    target_titles: list[str] | None = None
    target_seniority: list[str] | None = None
    target_geography: list[str] | None = None
    required_tech_stack: list[str] | None = None
    scoring_weights: dict | None = None
    custom_criteria: dict | None = None


class ICPCreate(ICPBase):
    pass


class ICPUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    target_industries: list[str] | None = None
    min_employee_count: int | None = None
    max_employee_count: int | None = None
    min_revenue: str | None = None
    max_revenue: str | None = None
    target_titles: list[str] | None = None
    target_seniority: list[str] | None = None
    target_geography: list[str] | None = None
    required_tech_stack: list[str] | None = None
    scoring_weights: dict | None = None
    custom_criteria: dict | None = None


class ICPResponse(ICPBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
