"""Pipeline Manager — supervisor agent that orchestrates the full pipeline."""

from crewai import Agent

from ai_sdr.config import settings


def create_pipeline_manager() -> Agent:
    return Agent(
        role="SDR Pipeline Orchestrator",
        goal=(
            "Coordinate the full pipeline from sourcing through appointment "
            "setting. Handle failures gracefully, track per-stage metrics, "
            "and produce a summary report."
        ),
        backstory=(
            "You are the VP of Sales Development overseeing the entire "
            "automated pipeline. You decide when to proceed, when to retry, "
            "and when to escalate. Quality always trumps quantity."
        ),
        tools=[],  # Supervisor delegates to other agents
        llm=f"{settings.LLM_PROVIDER}/{settings.LLM_MODEL_MID}",
        verbose=settings.DEBUG,
        allow_delegation=True,
    )
