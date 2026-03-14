"""Routing Rules API routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ai_sdr.api.v1.deps import get_db
from ai_sdr.schemas.routing_rule import RoutingRuleCreate, RoutingRuleResponse, RoutingRuleUpdate
from ai_sdr.services import routing_service

router = APIRouter()


@router.get("", response_model=list[RoutingRuleResponse])
async def list_routing_rules(
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    return await routing_service.list_routing_rules(db, active_only=active_only)


@router.post("", response_model=RoutingRuleResponse, status_code=201)
async def create_routing_rule(data: RoutingRuleCreate, db: AsyncSession = Depends(get_db)):
    return await routing_service.create_routing_rule(db, data)


@router.patch("/{rule_id}", response_model=RoutingRuleResponse)
async def update_routing_rule(
    rule_id: uuid.UUID,
    data: RoutingRuleUpdate,
    db: AsyncSession = Depends(get_db),
):
    rule = await routing_service.update_routing_rule(db, rule_id, data)
    if not rule:
        raise HTTPException(status_code=404, detail="Routing rule not found")
    return rule
