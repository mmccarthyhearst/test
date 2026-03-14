"""Lead service — CRUD and business logic for leads."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ai_sdr.models.lead import Lead, LeadStatus, LeadTier
from ai_sdr.schemas.lead import LeadCreate, LeadUpdate


async def create_lead(session: AsyncSession, data: LeadCreate) -> Lead:
    lead = Lead(**data.model_dump())
    session.add(lead)
    await session.commit()
    await session.refresh(lead)
    return lead


async def get_lead(session: AsyncSession, lead_id: uuid.UUID) -> Lead | None:
    result = await session.execute(
        select(Lead)
        .options(selectinload(Lead.company), selectinload(Lead.contact))
        .where(Lead.id == lead_id)
    )
    return result.scalar_one_or_none()


async def list_leads(
    session: AsyncSession,
    status: LeadStatus | None = None,
    tier: LeadTier | None = None,
    assigned_team: str | None = None,
    min_score: int | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Lead]:
    query = select(Lead)
    if status:
        query = query.where(Lead.status == status)
    if tier:
        query = query.where(Lead.tier == tier)
    if assigned_team:
        query = query.where(Lead.assigned_team == assigned_team)
    if min_score is not None:
        query = query.where(Lead.score >= min_score)
    query = query.order_by(Lead.created_at.desc()).limit(limit).offset(offset)
    result = await session.execute(query)
    return list(result.scalars().all())


async def update_lead(
    session: AsyncSession, lead_id: uuid.UUID, data: LeadUpdate
) -> Lead | None:
    lead = await session.get(Lead, lead_id)
    if not lead:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    await session.commit()
    await session.refresh(lead)
    return lead


async def disqualify_lead(
    session: AsyncSession, lead_id: uuid.UUID, reason: str
) -> Lead | None:
    lead = await session.get(Lead, lead_id)
    if not lead:
        return None
    lead.status = LeadStatus.DISQUALIFIED
    lead.disqualification_reason = reason
    await session.commit()
    await session.refresh(lead)
    return lead
