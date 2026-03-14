"""Lead Sourcer agent — discovers companies and contacts matching ICP."""

from crewai import Agent

from ai_sdr.config import settings
from ai_sdr.tools.crm import check_crm_duplicate
from ai_sdr.tools.enrichment import enrich_company, find_contacts
from ai_sdr.tools.web_scraper import scrape_website, search_companies


def create_lead_sourcer() -> Agent:
    return Agent(
        role="Lead Discovery Specialist",
        goal=(
            "Find companies and contacts matching the Ideal Customer Profile "
            "from web sources and enrichment APIs."
        ),
        backstory=(
            "You are an expert sales researcher who systematically searches "
            "industry databases, company websites, and professional networks "
            "to find high-quality leads. You always verify information and "
            "flag when data is uncertain."
        ),
        tools=[scrape_website, search_companies, enrich_company, find_contacts, check_crm_duplicate],
        llm=f"{settings.LLM_PROVIDER}/{settings.LLM_MODEL_FAST}",
        verbose=settings.DEBUG,
        max_iter=10,
    )
