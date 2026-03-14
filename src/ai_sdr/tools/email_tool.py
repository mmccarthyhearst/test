"""Email tool — SendGrid / Resend adapter."""

from crewai.tools import tool

from ai_sdr.config import settings


@tool
def send_email(to_email: str, subject: str, body: str) -> str:
    """Send an email to a prospect. Uses the configured email provider (SendGrid or Resend).

    Args:
        to_email: Recipient email address.
        subject: Email subject line.
        body: Email body (plain text or HTML).

    Returns:
        Confirmation with message ID, or error message.
    """
    if settings.EMAIL_PROVIDER == "sendgrid":
        return _send_via_sendgrid(to_email, subject, body)
    elif settings.EMAIL_PROVIDER == "resend":
        return _send_via_resend(to_email, subject, body)
    else:
        return f"Unknown email provider: {settings.EMAIL_PROVIDER}"


def _send_via_sendgrid(to_email: str, subject: str, body: str) -> str:
    if not settings.SENDGRID_API_KEY:
        return (
            f"[MOCK] Would send email via SendGrid:\n"
            f"To: {to_email}\nSubject: {subject}\nBody: {body[:200]}...\n"
            "Set SENDGRID_API_KEY to enable."
        )

    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        message = Mail(
            from_email=f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM_ADDRESS}>",
            to_emails=to_email,
            subject=subject,
            html_content=body,
        )
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        msg_id = response.headers.get("X-Message-Id", "unknown")
        return f"Email sent to {to_email}. Status: {response.status_code}, Message ID: {msg_id}"
    except Exception as e:
        return f"Error sending email via SendGrid: {e}"


def _send_via_resend(to_email: str, subject: str, body: str) -> str:
    if not settings.RESEND_API_KEY:
        return (
            f"[MOCK] Would send email via Resend:\n"
            f"To: {to_email}\nSubject: {subject}\nBody: {body[:200]}...\n"
            "Set RESEND_API_KEY to enable."
        )

    try:
        import resend

        resend.api_key = settings.RESEND_API_KEY
        result = resend.Emails.send(
            {
                "from": f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM_ADDRESS}>",
                "to": [to_email],
                "subject": subject,
                "html": body,
            }
        )
        return f"Email sent to {to_email}. Message ID: {result.get('id', 'unknown')}"
    except Exception as e:
        return f"Error sending email via Resend: {e}"
