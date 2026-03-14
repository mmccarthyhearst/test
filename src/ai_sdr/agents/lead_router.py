"""Lead Router agent — assigns leads to sales teams via routing rules."""

from crewai import Agent

from ai_sdr.config import settings
from ai_sdr.tools.crm import get_sales_reps


def create_lead_router() -> Agent:
    return Agent(
        role="Sales Pipeline Router",
        goal=(
            "Route each qualified lead to the right sales team or rep based "
            "on configurable routing rules, territory, and rep workload."
        ),
        backstory=(
            "You are a sales operations expert who ensures every qualified "
            "lead reaches the best-fit sales representative. You follow "
            "routing rules precisely and document your reasoning."
        ),
        tools=[get_sales_reps],
        llm=f"{settings.LLM_PROVIDER}/{settings.LLM_MODEL_FAST}",
        verbose=settings.DEBUG,
        max_iter=5,
    )
