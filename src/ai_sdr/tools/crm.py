"""CRM tool — Salesforce adapter via simple-salesforce."""

from crewai.tools import tool

from ai_sdr.config import settings


def _get_sf_client():
    """Create a Salesforce client. Returns None if credentials not configured."""
    if not all([settings.SALESFORCE_USERNAME, settings.SALESFORCE_PASSWORD]):
        return None

    from simple_salesforce import Salesforce

    return Salesforce(
        username=settings.SALESFORCE_USERNAME,
        password=settings.SALESFORCE_PASSWORD,
        security_token=settings.SALESFORCE_SECURITY_TOKEN,
        domain=settings.SALESFORCE_DOMAIN,
    )


@tool
def check_crm_duplicate(email: str) -> str:
    """Check if a contact already exists in Salesforce by email.

    Args:
        email: The email address to check.

    Returns:
        Whether the contact exists and any existing lead/opportunity data.
    """
    sf = _get_sf_client()
    if sf is None:
        return f"[MOCK] CRM check for {email}: No existing record found. Configure Salesforce credentials to enable live CRM checks."

    try:
        result = sf.query(
            f"SELECT Id, Name, Email, Account.Name FROM Contact WHERE Email = '{email}' LIMIT 1"
        )
        if result["totalSize"] > 0:
            record = result["records"][0]
            return (
                f"DUPLICATE FOUND: {record['Name']} at {record.get('Account', {}).get('Name', 'Unknown')} "
                f"(Salesforce ID: {record['Id']})"
            )
        return f"No existing record for {email} in Salesforce."
    except Exception as e:
        return f"Error checking CRM for {email}: {e}"


@tool
def create_crm_lead(
    first_name: str,
    last_name: str,
    email: str,
    company: str,
    title: str = "",
    description: str = "",
) -> str:
    """Create a new Lead record in Salesforce.

    Args:
        first_name: Contact's first name.
        last_name: Contact's last name.
        email: Contact's email.
        company: Company name.
        title: Contact's job title.
        description: Additional context about the lead.

    Returns:
        The Salesforce Lead ID if created, or error message.
    """
    sf = _get_sf_client()
    if sf is None:
        return f"[MOCK] Would create Salesforce lead: {first_name} {last_name} ({email}) at {company}. Configure Salesforce credentials to enable."

    try:
        result = sf.Lead.create(
            {
                "FirstName": first_name,
                "LastName": last_name,
                "Email": email,
                "Company": company,
                "Title": title,
                "Description": description,
                "LeadSource": "AI SDR",
            }
        )
        return f"Created Salesforce Lead: {result['id']}"
    except Exception as e:
        return f"Error creating lead in Salesforce: {e}"


@tool
def get_sales_reps(team: str = "") -> str:
    """Get a list of sales reps, optionally filtered by team.

    Args:
        team: Team name to filter by (optional).

    Returns:
        List of sales reps with their IDs and assignment info.
    """
    sf = _get_sf_client()
    if sf is None:
        return (
            "[MOCK] Sales reps:\n"
            "- Rep 1: Alice Johnson (alice@company.com) - Team: Enterprise\n"
            "- Rep 2: Bob Smith (bob@company.com) - Team: Mid-Market\n"
            "- Rep 3: Carol White (carol@company.com) - Team: SMB\n"
            "Configure Salesforce credentials for live data."
        )

    try:
        query = "SELECT Id, Name, Email, Department FROM User WHERE IsActive = true AND UserType = 'Standard'"
        if team:
            query += f" AND Department = '{team}'"
        query += " LIMIT 20"

        result = sf.query(query)
        if result["totalSize"] == 0:
            return f"No sales reps found for team: {team}"

        reps = []
        for r in result["records"]:
            reps.append(f"- {r['Name']} ({r['Email']}) - Dept: {r.get('Department', 'N/A')}")
        return "Sales reps:\n" + "\n".join(reps)
    except Exception as e:
        return f"Error fetching sales reps: {e}"
