"""Appointment Setter agent — crafts outreach and books meetings."""

from crewai import Agent

from ai_sdr.config import settings
from ai_sdr.tools.calendar import check_availability, create_booking
from ai_sdr.tools.crm import create_crm_lead
from ai_sdr.tools.email_tool import send_email
from ai_sdr.tools.slack import send_slack_notification


def create_appointment_setter() -> Agent:
    return Agent(
        role="Meeting Coordinator",
        goal=(
            "Craft personalized outreach emails and schedule introductory "
            "meetings between qualified leads and their assigned sales reps."
        ),
        backstory=(
            "You are a skilled SDR who writes compelling, personalized "
            "outreach emails. Good outreach references specific pain points, "
            "recent company events, and offers clear value — never generic "
            "templates. You handle scheduling logistics seamlessly."
        ),
        tools=[
            send_email,
            check_availability,
            create_booking,
            create_crm_lead,
            send_slack_notification,
        ],
        llm=f"{settings.LLM_PROVIDER}/{settings.LLM_MODEL_MID}",
        verbose=settings.DEBUG,
        max_iter=10,
    )
