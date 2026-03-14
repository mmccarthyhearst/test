"""Outreach model - messages sent to prospects."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ai_sdr.db.base import Base
from ai_sdr.db.mixins import TimestampMixin


class OutreachChannel(str, enum.Enum):
    EMAIL = "email"
    LINKEDIN = "linkedin"


class OutreachStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    REPLIED = "replied"
    BOUNCED = "bounced"


class Outreach(TimestampMixin, Base):
    __tablename__ = "outreach"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id"), nullable=False
    )

    channel: Mapped[OutreachChannel] = mapped_column(Enum(OutreachChannel), nullable=False)
    sequence_step: Mapped[int] = mapped_column(Integer, default=1)
    subject: Mapped[str | None] = mapped_column(String(500))
    body: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[OutreachStatus] = mapped_column(
        Enum(OutreachStatus), default=OutreachStatus.DRAFT
    )
    external_message_id: Mapped[str | None] = mapped_column(String(255))

    # Relationships
    lead: Mapped["Lead"] = relationship(back_populates="outreach_messages")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Outreach {self.channel.value} step={self.sequence_step} status={self.status.value}>"
