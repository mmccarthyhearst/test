"""CrewAI orchestrator — wires agents and tasks into the SDR pipeline crew."""

from crewai import Crew, Process, Task

from ai_sdr.agents.appointment_setter import create_appointment_setter
from ai_sdr.agents.lead_qualifier import create_lead_qualifier
from ai_sdr.agents.lead_router import create_lead_router
from ai_sdr.agents.lead_sourcer import create_lead_sourcer
from ai_sdr.agents.pipeline_manager import create_pipeline_manager


def create_sdr_crew(
    icp_criteria: str,
    scoring_weights: str = "{}",
    routing_rules: str = "[]",
    max_leads: int = 10,
) -> Crew:
    """Create and return the full SDR pipeline crew.

    Args:
        icp_criteria: JSON string describing the Ideal Customer Profile.
        scoring_weights: JSON string of scoring weights per criterion.
        routing_rules: JSON string of routing rules for lead assignment.
        max_leads: Maximum number of leads to source per run.

    Returns:
        A configured CrewAI Crew ready to kickoff.
    """
    # Create agents
    sourcer = create_lead_sourcer()
    qualifier = create_lead_qualifier()
    router = create_lead_router()
    setter = create_appointment_setter()
    manager = create_pipeline_manager()

    # Define tasks
    source_task = Task(
        description=(
            f"Search for companies and contacts matching this ICP criteria:\n"
            f"{icp_criteria}\n\n"
            f"Find up to {max_leads} lead candidates. For each candidate, gather:\n"
            "- Company name, domain, industry, size, and location\n"
            "- At least one contact with name, email, title, and seniority\n"
            "- Check the CRM for duplicates before including\n\n"
            "Return results as a JSON list of lead candidates."
        ),
        expected_output="A JSON array of lead candidates with company and contact details.",
        agent=sourcer,
    )

    qualify_task = Task(
        description=(
            f"Score and qualify each lead candidate against the ICP:\n"
            f"{icp_criteria}\n\n"
            f"Scoring weights: {scoring_weights}\n\n"
            "For each candidate:\n"
            "1. Research for buying signals (funding, hiring, tech adoption)\n"
            "2. Score from 0-100 based on ICP fit\n"
            "3. Assign tier: Hot (80+), Warm (50-79), Cold (<50)\n"
            "4. Document your reasoning"
        ),
        expected_output="A JSON array of qualified leads with score, tier, reasoning, and buying signals.",
        agent=qualifier,
        context=[source_task],
    )

    route_task = Task(
        description=(
            f"Route each qualified lead to the appropriate sales team using these rules:\n"
            f"{routing_rules}\n\n"
            "Evaluate rules in priority order (lower number = higher priority). "
            "Use the first matching rule. If no rule matches, assign to default team."
        ),
        expected_output="A JSON array of routed leads with assigned team, rep, and reasoning.",
        agent=router,
        context=[qualify_task],
    )

    appointment_task = Task(
        description=(
            "For each routed lead:\n"
            "1. Write a personalized outreach email referencing specific company context\n"
            "2. Check calendar availability for the assigned rep\n"
            "3. Include a booking link in the email\n"
            "4. Send the email\n"
            "5. Notify the assigned rep via Slack"
        ),
        expected_output="A JSON array of outreach results with email status and booking details.",
        agent=setter,
        context=[route_task],
    )

    # Create the crew with hierarchical process
    crew = Crew(
        agents=[sourcer, qualifier, router, setter],
        tasks=[source_task, qualify_task, route_task, appointment_task],
        manager_agent=manager,
        process=Process.hierarchical,
        verbose=True,
    )

    return crew
