"""Calendar tool — Cal.com API v2 adapter."""

import httpx
from crewai.tools import tool

from ai_sdr.config import settings


def _cal_headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.CALCOM_API_KEY}",
        "Content-Type": "application/json",
        "cal-api-version": "2024-08-13",
    }


@tool
def check_availability(date: str, duration_minutes: int = 30) -> str:
    """Check calendar availability for a given date. Returns available time slots.

    Args:
        date: Date to check in YYYY-MM-DD format.
        duration_minutes: Duration of the meeting in minutes.

    Returns:
        List of available time slots, or error message.
    """
    if not settings.CALCOM_API_KEY:
        return (
            f"[MOCK] Available slots on {date} ({duration_minutes}min):\n"
            "- 9:00 AM - 9:30 AM\n- 10:00 AM - 10:30 AM\n"
            "- 2:00 PM - 2:30 PM\n- 4:00 PM - 4:30 PM\n"
            "Set CALCOM_API_KEY to enable live scheduling."
        )

    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.get(
                f"{settings.CALCOM_BASE_URL}/slots",
                headers=_cal_headers(),
                params={
                    "startTime": f"{date}T00:00:00Z",
                    "endTime": f"{date}T23:59:59Z",
                    "duration": duration_minutes,
                },
            )
            response.raise_for_status()
            data = response.json()
            slots = data.get("data", {}).get("slots", {})

            if not slots:
                return f"No available slots on {date}"

            result = f"Available slots on {date}:\n"
            for date_key, time_slots in slots.items():
                for slot in time_slots:
                    result += f"- {slot.get('time', 'Unknown')}\n"
            return result
    except Exception as e:
        return f"Error checking availability: {e}"


@tool
def create_booking(
    start_time: str,
    attendee_name: str,
    attendee_email: str,
    notes: str = "",
) -> str:
    """Book a meeting on Cal.com.

    Args:
        start_time: Meeting start time in ISO format (e.g., '2024-01-15T10:00:00Z').
        attendee_name: Name of the person being invited.
        attendee_email: Email of the person being invited.
        notes: Optional meeting notes or agenda.

    Returns:
        Booking confirmation with meeting link, or error message.
    """
    if not settings.CALCOM_API_KEY:
        return (
            f"[MOCK] Would book meeting:\n"
            f"Time: {start_time}\nAttendee: {attendee_name} ({attendee_email})\n"
            f"Notes: {notes}\nMeeting link: https://cal.com/mock/meeting-123\n"
            "Set CALCOM_API_KEY to enable live booking."
        )

    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.post(
                f"{settings.CALCOM_BASE_URL}/bookings",
                headers=_cal_headers(),
                json={
                    "start": start_time,
                    "attendee": {
                        "name": attendee_name,
                        "email": attendee_email,
                    },
                    "metadata": {"notes": notes, "source": "ai-sdr"},
                },
            )
            response.raise_for_status()
            data = response.json()
            booking = data.get("data", {})
            return (
                f"Meeting booked!\n"
                f"ID: {booking.get('id', 'unknown')}\n"
                f"Time: {booking.get('startTime', start_time)}\n"
                f"Link: {booking.get('meetingUrl', 'N/A')}"
            )
    except Exception as e:
        return f"Error creating booking: {e}"
