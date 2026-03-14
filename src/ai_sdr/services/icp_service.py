"""ICP service — CRUD and scoring logic for Ideal Customer Profiles."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_sdr.models.icp import ICP
from ai_sdr.schemas.agent import LeadCandidate
from ai_sdr.schemas.icp import ICPCreate, ICPUpdate


async def create_icp(session: AsyncSession, data: ICPCreate) -> ICP:
    icp = ICP(**data.model_dump())
    session.add(icp)
    await session.commit()
    await session.refresh(icp)
    return icp


async def get_icp(session: AsyncSession, icp_id: uuid.UUID) -> ICP | None:
    return await session.get(ICP, icp_id)


async def list_icps(
    session: AsyncSession, active_only: bool = True
) -> list[ICP]:
    query = select(ICP)
    if active_only:
        query = query.where(ICP.is_active == True)  # noqa: E712
    query = query.order_by(ICP.created_at.desc())
    result = await session.execute(query)
    return list(result.scalars().all())


async def update_icp(
    session: AsyncSession, icp_id: uuid.UUID, data: ICPUpdate
) -> ICP | None:
    icp = await session.get(ICP, icp_id)
    if not icp:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(icp, field, value)
    await session.commit()
    await session.refresh(icp)
    return icp


def score_lead_against_icp(candidate: LeadCandidate, icp: ICP) -> int:
    """Score a lead candidate (0-100) against an ICP definition.

    This is deterministic business logic — NOT done by the LLM.
    The LLM agent calls this function for consistent scoring.
    """
    score = 0
    max_possible = 0
    weights = icp.scoring_weights or {}

    # Industry match
    weight = weights.get("industry", 20)
    if icp.target_industries:
        max_possible += weight
    if icp.target_industries and candidate.industry:
        if candidate.industry.lower() in [i.lower() for i in icp.target_industries]:
            score += weight

    # Company size match
    weight = weights.get("company_size", 20)
    if icp.min_employee_count is not None or icp.max_employee_count is not None:
        max_possible += weight
    if candidate.employee_count_range and icp.min_employee_count is not None:
        try:
            # Parse ranges like "50-200", "1000+"
            range_str = candidate.employee_count_range.replace("+", "-999999")
            parts = range_str.split("-")
            low = int(parts[0].strip())
            high = int(parts[1].strip()) if len(parts) > 1 else low
            midpoint = (low + high) // 2

            min_emp = icp.min_employee_count or 0
            max_emp = icp.max_employee_count or 999999
            if min_emp <= midpoint <= max_emp:
                score += weight
            elif min_emp <= low <= max_emp or min_emp <= high <= max_emp:
                score += weight // 2  # Partial match
        except (ValueError, IndexError):
            pass

    # Seniority match
    weight = weights.get("seniority", 20)
    if icp.target_seniority:
        max_possible += weight
    if icp.target_seniority and candidate.contact_seniority:
        if candidate.contact_seniority.lower() in [s.lower() for s in icp.target_seniority]:
            score += weight

    # Title match
    weight = weights.get("title", 15)
    if icp.target_titles:
        max_possible += weight
    if icp.target_titles and candidate.contact_title:
        title_lower = candidate.contact_title.lower()
        for target_title in icp.target_titles:
            if target_title.lower() in title_lower:
                score += weight
                break

    # Geography match
    weight = weights.get("geography", 10)
    if icp.target_geography:
        max_possible += weight
    if icp.target_geography and candidate.hq_location:
        loc_lower = candidate.hq_location.lower()
        for geo in icp.target_geography:
            if geo.lower() in loc_lower:
                score += weight
                break

    # Tech stack match
    weight = weights.get("tech_stack", 15)
    if icp.required_tech_stack:
        max_possible += weight
    if icp.required_tech_stack and candidate.tech_stack:
        candidate_tech = {t.lower() for t in candidate.tech_stack}
        required_tech = {t.lower() for t in icp.required_tech_stack}
        overlap = candidate_tech & required_tech
        if overlap:
            ratio = len(overlap) / len(required_tech)
            score += int(weight * ratio)

    # Normalize to 0-100
    if max_possible > 0:
        return min(100, int((score / max_possible) * 100))
    return 50  # Default if no criteria defined
