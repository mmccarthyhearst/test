"""Slack notification tool."""

import httpx
from crewai.tools import tool

from ai_sdr.config import settings


@tool
def send_slack_notification(message: str) -> str:
    """Send a notification to Slack. Used to alert sales reps about new leads
    or booked meetings.

    Args:
        message: The notification message to send.

    Returns:
        Confirmation or error message.
    """
    if not settings.SLACK_WEBHOOK_URL:
        return f"[MOCK] Would send Slack notification: {message[:200]}. Set SLACK_WEBHOOK_URL to enable."

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                settings.SLACK_WEBHOOK_URL,
                json={"text": message},
            )
            response.raise_for_status()
            return "Slack notification sent successfully."
    except Exception as e:
        return f"Error sending Slack notification: {e}"
