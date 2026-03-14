"""Company API routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ai_sdr.api.v1.deps import get_db
from ai_sdr.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from ai_sdr.services import company_service

router = APIRouter()


@router.get("", response_model=list[CompanyResponse])
async def list_companies(
    industry: str | None = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    return await company_service.list_companies(db, industry=industry, limit=limit, offset=offset)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    company = await company_service.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("", response_model=CompanyResponse, status_code=201)
async def create_company(data: CompanyCreate, db: AsyncSession = Depends(get_db)):
    return await company_service.create_company(db, data)


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: uuid.UUID, data: CompanyUpdate, db: AsyncSession = Depends(get_db)
):
    company = await company_service.update_company(db, company_id, data)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
