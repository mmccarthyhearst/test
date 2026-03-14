"""Background tasks for pipeline execution via ARQ."""

import json
import logging

from ai_sdr.agents.crew import create_sdr_crew

logger = logging.getLogger(__name__)


async def run_pipeline(ctx: dict, run_id: str, crew_inputs: dict) -> dict:
    """Execute a full SDR pipeline run in the background.

    This task is enqueued by the pipeline API endpoint and executed
    by the ARQ worker. It creates the CrewAI crew and kicks off execution.

    Args:
        ctx: ARQ context (contains Redis connection).
        run_id: UUID string of the AgentRun record.
        crew_inputs: Dict with icp_criteria, scoring_weights, routing_rules, max_leads.

    Returns:
        Dict with execution results.
    """
    logger.info(f"Starting pipeline run {run_id}")

    try:
        crew = create_sdr_crew(
            icp_criteria=crew_inputs["icp_criteria"],
            scoring_weights=crew_inputs.get("scoring_weights", "{}"),
            routing_rules=crew_inputs.get("routing_rules", "[]"),
            max_leads=crew_inputs.get("max_leads", 10),
        )

        result = crew.kickoff()

        logger.info(f"Pipeline run {run_id} completed successfully")
        return {
            "run_id": run_id,
            "status": "completed",
            "result": str(result),
        }
    except Exception as e:
        logger.error(f"Pipeline run {run_id} failed: {e}")
        return {
            "run_id": run_id,
            "status": "failed",
            "error": str(e),
        }


class WorkerSettings:
    """ARQ worker settings."""

    functions = [run_pipeline]
    redis_settings = None  # Set from config at startup
