"""Lead enrichment tool — Apollo.io adapter (and future enrichment APIs)."""

import httpx
from crewai.tools import tool

from ai_sdr.config import settings


@tool
def enrich_company(domain: str) -> str:
    """Enrich company data by looking up a domain. Returns company information
    including industry, size, funding, and tech stack.

    Args:
        domain: Company website domain (e.g., 'acme.com').

    Returns:
        JSON-formatted company enrichment data, or error message.
    """
    if not settings.APOLLO_API_KEY:
        return (
            f"[MOCK] Enrichment for {domain}: "
            "Industry: Technology, Employees: 50-200, Revenue: $10M-$50M, "
            "Funding: Series B, Tech: Python, AWS, Salesforce. "
            "Set APOLLO_API_KEY to enable live enrichment."
        )

    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.post(
                "https://api.apollo.io/v1/organizations/enrich",
                headers={"x-api-key": settings.APOLLO_API_KEY},
                json={"domain": domain},
            )
            response.raise_for_status()
            data = response.json()
            org = data.get("organization", {})
            return (
                f"Company: {org.get('name', 'Unknown')}\n"
                f"Industry: {org.get('industry', 'Unknown')}\n"
                f"Employees: {org.get('estimated_num_employees', 'Unknown')}\n"
                f"Revenue: {org.get('annual_revenue_printed', 'Unknown')}\n"
                f"Founded: {org.get('founded_year', 'Unknown')}\n"
                f"Description: {org.get('short_description', 'N/A')}\n"
                f"Tech: {', '.join(org.get('technology_names', [])[:10])}"
            )
    except Exception as e:
        return f"Error enriching {domain}: {e}"


@tool
def find_contacts(domain: str, title_keywords: str = "") -> str:
    """Find contacts at a company by domain. Optionally filter by title keywords.

    Args:
        domain: Company website domain.
        title_keywords: Comma-separated keywords to filter titles (e.g., 'VP, Director, Sales').

    Returns:
        List of contacts found, or error message.
    """
    if not settings.APOLLO_API_KEY:
        return (
            f"[MOCK] Contacts at {domain} (filter: {title_keywords}): "
            "1. Jane Smith, VP of Sales, jane@example.com | "
            "2. John Doe, Director of Revenue, john@example.com. "
            "Set APOLLO_API_KEY to enable live contact search."
        )

    try:
        titles = [t.strip() for t in title_keywords.split(",") if t.strip()]
        with httpx.Client(timeout=15.0) as client:
            payload = {
                "q_organization_domains": domain,
                "per_page": 5,
            }
            if titles:
                payload["person_titles"] = titles

            response = client.post(
                "https://api.apollo.io/v1/mixed_people/search",
                headers={"x-api-key": settings.APOLLO_API_KEY},
                json=payload,
            )
            response.raise_for_status()
            people = response.json().get("people", [])

            if not people:
                return f"No contacts found at {domain}"

            results = []
            for p in people[:5]:
                results.append(
                    f"- {p.get('first_name', '')} {p.get('last_name', '')}, "
                    f"{p.get('title', 'N/A')}, {p.get('email', 'N/A')}"
                )
            return f"Contacts at {domain}:\n" + "\n".join(results)
    except Exception as e:
        return f"Error finding contacts at {domain}: {e}"
