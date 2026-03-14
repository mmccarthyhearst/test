"""RoutingRule model - configurable rules for lead triage."""

import uuid

from sqlalchemy import Boolean, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ai_sdr.db.base import Base
from ai_sdr.db.mixins import TimestampMixin


class RoutingRule(TimestampMixin, Base):
    __tablename__ = "routing_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[int] = mapped_column(Integer, default=0)  # Lower = higher priority
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Conditions: list of {"field": ..., "op": ..., "value": ...}
    conditions: Mapped[list] = mapped_column(JSON, nullable=False)

    # Action: {"team": "...", "rep_id": "...", "rep_name": "..."}
    action: Mapped[dict] = mapped_column(JSON, nullable=False)

    def __repr__(self) -> str:
        return f"<RoutingRule {self.name} priority={self.priority}>"
