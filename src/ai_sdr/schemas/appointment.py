"""Appointment schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from ai_sdr.models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    lead_id: uuid.UUID
    scheduled_at: datetime
    duration_minutes: int = 30
    meeting_type: str = "intro_call"
    meeting_link: str | None = None
    rep_email: str
    prospect_email: str
    notes: str | None = None


class AppointmentUpdate(BaseModel):
    scheduled_at: datetime | None = None
    status: AppointmentStatus | None = None
    meeting_link: str | None = None
    notes: str | None = None


class AppointmentResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    calendar_event_id: str | None
    scheduled_at: datetime
    duration_minutes: int
    meeting_type: str
    meeting_link: str | None
    status: AppointmentStatus
    rep_email: str
    prospect_email: str
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
