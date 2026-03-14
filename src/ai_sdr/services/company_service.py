"""Company service — CRUD operations for companies."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_sdr.models.company import Company
from ai_sdr.schemas.company import CompanyCreate, CompanyUpdate


async def create_company(session: AsyncSession, data: CompanyCreate) -> Company:
    company = Company(**data.model_dump())
    session.add(company)
    await session.commit()
    await session.refresh(company)
    return company


async def get_company(session: AsyncSession, company_id: uuid.UUID) -> Company | None:
    return await session.get(Company, company_id)


async def get_company_by_domain(session: AsyncSession, domain: str) -> Company | None:
    result = await session.execute(select(Company).where(Company.domain == domain))
    return result.scalar_one_or_none()


async def list_companies(
    session: AsyncSession,
    industry: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Company]:
    query = select(Company)
    if industry:
        query = query.where(Company.industry == industry)
    query = query.order_by(Company.created_at.desc()).limit(limit).offset(offset)
    result = await session.execute(query)
    return list(result.scalars().all())


async def update_company(
    session: AsyncSession, company_id: uuid.UUID, data: CompanyUpdate
) -> Company | None:
    company = await session.get(Company, company_id)
    if not company:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    await session.commit()
    await session.refresh(company)
    return company
