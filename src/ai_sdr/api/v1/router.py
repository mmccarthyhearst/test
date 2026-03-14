"""Aggregate API v1 router."""

from fastapi import APIRouter

from ai_sdr.api.v1 import appointments, companies, icp, leads, pipeline, routing_rules

api_router = APIRouter()

api_router.include_router(leads.router, prefix="/leads", tags=["Leads"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(icp.router, prefix="/icp", tags=["ICP"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])
api_router.include_router(routing_rules.router, prefix="/routing-rules", tags=["Routing Rules"])
