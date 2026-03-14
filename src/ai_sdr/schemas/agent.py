"""Agent contract schemas - typed data flowing between agents in the pipeline.

These are the CRITICAL typed contracts that prevent cascade failures
between agents. Every agent's output is validated through these schemas
before being passed to the next agent.
"""

from pydantic import BaseModel


# ── Lead Sourcer → Lead Qualifier ──────────────────────────────────────


class LeadCandidate(BaseModel):
    """Output of Lead Sourcer agent. A raw prospect found via scraping/enrichment."""

    company_name: str
    company_domain: str
    industry: str | None = None
    employee_count_range: str | None = None
    estimated_revenue: str | None = None
    hq_location: str | None = None
    tech_stack: list[str] | None = None
    description: str | None = None

    # Contact info
    contact_first_name: str
    contact_last_name: str
    contact_email: str
    contact_title: str | None = None
    contact_seniority: str | None = None
    contact_linkedin_url: str | None = None

    source: str = "web_scrape"
    source_url: str | None = None


# ── Lead Qualifier → Lead Router ───────────────────────────────────────


class BuyingSignal(BaseModel):
    """A detected buying signal for a lead."""

    signal_type: str  # "funding", "hiring", "tech_adoption", "expansion", etc.
    description: str
    confidence: float  # 0.0 - 1.0
    source: str | None = None


class QualifiedLead(BaseModel):
    """Output of Lead Qualifier agent. A scored and tiered lead."""

    candidate: LeadCandidate
    score: int  # 0-100
    tier: str  # "hot", "warm", "cold"
    qualification_reasoning: str
    buying_signals: list[BuyingSignal] = []
    meets_icp: bool = True


# ── Lead Router → Appointment Setter ───────────────────────────────────


class RoutedLead(BaseModel):
    """Output of Lead Router agent. A qualified lead assigned to a team/rep."""

    qualified_lead: QualifiedLead
    assigned_team: str
    assigned_rep_id: str | None = None
    assigned_rep_name: str | None = None
    assigned_rep_email: str | None = None
    routing_reasoning: str


# ── Appointment Setter → Pipeline Results ──────────────────────────────


class OutreachResult(BaseModel):
    """Output of Appointment Setter agent. Result of outreach attempt."""

    routed_lead: RoutedLead
    email_sent: bool = False
    email_subject: str | None = None
    email_body: str | None = None
    meeting_booked: bool = False
    meeting_datetime: str | None = None
    meeting_link: str | None = None
    follow_up_scheduled: bool = False
    notes: str | None = None


# ── Pipeline Run Request ───────────────────────────────────────────────


class PipelineRunRequest(BaseModel):
    """Request to trigger a new pipeline run."""

    icp_id: str | None = None
    max_leads: int = 10
    dry_run: bool = False


class PipelineRunResponse(BaseModel):
    """Response after triggering a pipeline run."""

    run_id: str
    status: str
    message: str
