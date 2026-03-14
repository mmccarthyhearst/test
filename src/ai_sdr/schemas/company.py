"""Company schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, HttpUrl


class CompanyBase(BaseModel):
    name: str
    domain: str
    industry: str | None = None
    employee_count_range: str | None = None
    estimated_revenue: str | None = None
    hq_location: str | None = None
    tech_stack: list[str] | None = None
    funding_stage: str | None = None
    last_funding_amount: str | None = None
    description: str | None = None
    linkedin_url: str | None = None


class CompanyCreate(CompanyBase):
    source: str = "manual"


class CompanyUpdate(BaseModel):
    name: str | None = None
    industry: str | None = None
    employee_count_range: str | None = None
    estimated_revenue: str | None = None
    hq_location: str | None = None
    tech_stack: list[str] | None = None
    funding_stage: str | None = None
    description: str | None = None
    crm_id: str | None = None


class CompanyResponse(CompanyBase):
    id: uuid.UUID
    crm_id: str | None = None
    source: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
