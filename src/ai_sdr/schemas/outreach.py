"""Outreach schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from ai_sdr.models.outreach import OutreachChannel, OutreachStatus


class OutreachCreate(BaseModel):
    lead_id: uuid.UUID
    channel: OutreachChannel
    sequence_step: int = 1
    subject: str | None = None
    body: str


class OutreachResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    channel: OutreachChannel
    sequence_step: int
    subject: str | None
    body: str
    sent_at: datetime | None
    status: OutreachStatus
    external_message_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
