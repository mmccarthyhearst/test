"""Lead Qualifier agent — scores leads against ICP criteria."""

from crewai import Agent

from ai_sdr.config import settings
from ai_sdr.tools.enrichment import enrich_company
from ai_sdr.tools.web_scraper import scrape_website


def create_lead_qualifier() -> Agent:
    return Agent(
        role="Lead Qualification Analyst",
        goal=(
            "Score each lead candidate against ICP criteria. Identify buying "
            "signals and assign a qualification tier (Hot/Warm/Cold) with "
            "clear reasoning."
        ),
        backstory=(
            "You are a meticulous sales analyst who evaluates prospects against "
            "strict criteria. You look for buying signals such as recent funding, "
            "hiring activity, technology adoption, and expansion indicators. "
            "Accuracy matters more than volume."
        ),
        tools=[enrich_company, scrape_website],
        llm=f"{settings.LLM_PROVIDER}/{settings.LLM_MODEL_MID}",
        verbose=settings.DEBUG,
        max_iter=10,
    )
