"""Pipeline service — triggers and manages agent pipeline runs."""

import json
import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from ai_sdr.models.agent_run import AgentRun, AgentRunStatus
from ai_sdr.models.icp import ICP
from ai_sdr.services.routing_service import list_routing_rules


async def create_pipeline_run(
    session: AsyncSession,
    icp_id: uuid.UUID | None = None,
    trigger: str = "manual",
) -> AgentRun:
    """Create a new pipeline run record."""
    run = AgentRun(
        status=AgentRunStatus.PENDING,
        trigger=trigger,
        icp_id=icp_id,
    )
    session.add(run)
    await session.commit()
    await session.refresh(run)
    return run


async def start_pipeline_run(session: AsyncSession, run_id: uuid.UUID) -> AgentRun | None:
    """Mark a pipeline run as started."""
    run = await session.get(AgentRun, run_id)
    if not run:
        return None
    run.status = AgentRunStatus.RUNNING
    run.started_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(run)
    return run


async def complete_pipeline_run(
    session: AsyncSession,
    run_id: uuid.UUID,
    leads_sourced: int = 0,
    leads_qualified: int = 0,
    leads_routed: int = 0,
    appointments_set: int = 0,
) -> AgentRun | None:
    """Mark a pipeline run as completed with metrics."""
    run = await session.get(AgentRun, run_id)
    if not run:
        return None
    run.status = AgentRunStatus.COMPLETED
    run.completed_at = datetime.now(timezone.utc)
    run.leads_sourced = leads_sourced
    run.leads_qualified = leads_qualified
    run.leads_routed = leads_routed
    run.appointments_set = appointments_set
    await session.commit()
    await session.refresh(run)
    return run


async def fail_pipeline_run(
    session: AsyncSession, run_id: uuid.UUID, error_message: str
) -> AgentRun | None:
    """Mark a pipeline run as failed."""
    run = await session.get(AgentRun, run_id)
    if not run:
        return None
    run.status = AgentRunStatus.FAILED
    run.completed_at = datetime.now(timezone.utc)
    run.error_message = error_message
    await session.commit()
    await session.refresh(run)
    return run


async def prepare_crew_inputs(
    session: AsyncSession,
    icp: ICP,
    max_leads: int = 10,
) -> dict:
    """Prepare the inputs needed to kickoff the SDR crew.

    Returns a dict with icp_criteria, scoring_weights, and routing_rules
    serialized as JSON strings for the crew tasks.
    """
    # Build ICP criteria dict
    icp_criteria = {
        "name": icp.name,
        "target_industries": icp.target_industries or [],
        "min_employee_count": icp.min_employee_count,
        "max_employee_count": icp.max_employee_count,
        "target_titles": icp.target_titles or [],
        "target_seniority": icp.target_seniority or [],
        "target_geography": icp.target_geography or [],
        "required_tech_stack": icp.required_tech_stack or [],
        "custom_criteria": icp.custom_criteria or {},
    }

    # Get active routing rules
    rules = await list_routing_rules(session, active_only=True)
    routing_rules = [
        {"name": r.name, "priority": r.priority, "conditions": r.conditions, "action": r.action}
        for r in rules
    ]

    return {
        "icp_criteria": json.dumps(icp_criteria, indent=2),
        "scoring_weights": json.dumps(icp.scoring_weights or {}, indent=2),
        "routing_rules": json.dumps(routing_rules, indent=2),
        "max_leads": max_leads,
    }
