"""Web scraping tool for lead discovery."""

import asyncio
import time

import httpx
from bs4 import BeautifulSoup
from crewai.tools import tool

from ai_sdr.config import settings

_last_request_time = 0.0


def _rate_limit():
    """Simple rate limiter for scraping."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < settings.SCRAPER_RATE_LIMIT_SECONDS:
        time.sleep(settings.SCRAPER_RATE_LIMIT_SECONDS - elapsed)
    _last_request_time = time.time()


@tool
def scrape_website(url: str) -> str:
    """Scrape a website URL and return its text content. Useful for researching
    companies and finding contact information on their websites.

    Args:
        url: The URL to scrape.

    Returns:
        The text content of the page, or an error message.
    """
    _rate_limit()
    try:
        with httpx.Client(
            headers={"User-Agent": settings.SCRAPER_USER_AGENT},
            follow_redirects=True,
            timeout=15.0,
        ) as client:
            response = client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        # Truncate to avoid context overflow
        return text[:8000]
    except Exception as e:
        return f"Error scraping {url}: {e}"


@tool
def search_companies(query: str, max_results: int = 5) -> str:
    """Search the web for companies matching a query. Returns a list of company
    names and domains found.

    Args:
        query: Search query describing the type of companies to find.
        max_results: Maximum number of results to return.

    Returns:
        Text description of companies found, or error message.
    """
    # This is a stub — in production, integrate with a search API
    # (Serper, BrightData, SerpAPI) or use Firecrawl
    return (
        f"[STUB] Would search for: '{query}' (max {max_results} results). "
        "Configure a search API (Serper, BrightData) to enable live search. "
        "For now, use scrape_website with specific URLs."
    )
