"""Seed data for the Sales Assistant agent.

These fixtures stand in for the systems a real sales assistant would talk to:
a CRM (Salesforce), an opportunity pipeline, and an internal knowledge base.
Everything is in-memory so the agent is easy to run and reason about. The tools
in ``tools.py`` read from (and pretend to write to) these dictionaries.
"""

# ---------------------------------------------------------------------------
# CRM accounts (what `lookup_customer` searches)
# ---------------------------------------------------------------------------
ACCOUNTS = {
    "ACC-1001": {
        "id": "ACC-1001",
        "name": "Northwind Trading",
        "industry": "Logistics",
        "tier": "Enterprise",
        "primary_contact": {"name": "Dana Ruiz", "email": "dana.ruiz@northwind.example"},
        "renewal_date": "2026-09-30",
        "arr_usd": 240000,
        "notes": "Expanding into EU. Sensitive about data residency.",
    },
    "ACC-1002": {
        "id": "ACC-1002",
        "name": "Halcyon Health",
        "industry": "Healthcare",
        "tier": "Enterprise",
        "primary_contact": {"name": "Sam Okoro", "email": "sam.okoro@halcyon.example"},
        "renewal_date": "2026-08-15",
        "arr_usd": 180000,
        "notes": "Requires HIPAA coverage. Evaluating two competitors.",
    },
    "ACC-1003": {
        "id": "ACC-1003",
        "name": "Bright Peak Media",
        "industry": "Media",
        "tier": "Mid-Market",
        "primary_contact": {"name": "Alex Chen", "email": "alex.chen@brightpeak.example"},
        "renewal_date": "2026-11-01",
        "arr_usd": 60000,
        "notes": "Champion recently changed roles. Need to re-establish contact.",
    },
    "ACC-1004": {
        "id": "ACC-1004",
        "name": "Cobalt Robotics",
        "industry": "Manufacturing",
        "tier": "Enterprise",
        "primary_contact": {"name": "Priya Nair", "email": "priya.nair@cobalt.example"},
        "renewal_date": "2026-12-31",
        "arr_usd": 320000,
        "notes": "Heavy API usage. Interested in on-prem deployment options.",
    },
    "ACC-1005": {
        "id": "ACC-1005",
        "name": "Willow Financial",
        "industry": "Financial Services",
        "tier": "Enterprise",
        "primary_contact": {"name": "Marcus Bell", "email": "marcus.bell@willowfin.example"},
        "renewal_date": "2026-07-31",
        "arr_usd": 210000,
        "notes": "Renewal at risk. Budget freeze under review by new CFO.",
    },
    "ACC-1006": {
        "id": "ACC-1006",
        "name": "Fernwood Labs",
        "industry": "Biotech",
        "tier": "Mid-Market",
        "primary_contact": {"name": "Lena Petrov", "email": "lena.petrov@fernwood.example"},
        "renewal_date": "2026-10-05",
        "arr_usd": 48000,
        "notes": "Fast-growing team. Strong candidate for tier upgrade.",
    },
    "ACC-1007": {
        "id": "ACC-1007",
        "name": "Summit Gear Co",
        "industry": "Retail",
        "tier": "SMB",
        "primary_contact": {"name": "Owen Diaz", "email": "owen.diaz@summitgear.example"},
        "renewal_date": "2026-09-12",
        "arr_usd": 24000,
        "notes": "Price sensitive. Responds well to annual prepay incentives.",
    },
}

# ---------------------------------------------------------------------------
# Opportunities (what `get_opportunity` returns)
# ---------------------------------------------------------------------------
OPPORTUNITIES = {
    "OPP-5001": {
        "id": "OPP-5001",
        "account_id": "ACC-1001",
        "name": "Northwind EU expansion",
        "stage": "Negotiation",
        "amount_usd": 90000,
        "close_date": "2026-08-20",
        "next_step": "Send revised pricing with EU data residency addendum.",
    },
    "OPP-5002": {
        "id": "OPP-5002",
        "account_id": "ACC-1002",
        "name": "Halcyon platform upsell",
        "stage": "Proposal",
        "amount_usd": 45000,
        "close_date": "2026-08-10",
        "next_step": "Confirm HIPAA BAA is signed before proposal review.",
    },
    "OPP-5003": {
        "id": "OPP-5003",
        "account_id": "ACC-1003",
        "name": "Bright Peak renewal",
        "stage": "Discovery",
        "amount_usd": 60000,
        "close_date": "2026-10-15",
        "next_step": "Identify new champion after the reorg.",
    },
    "OPP-5004": {
        "id": "OPP-5004",
        "account_id": "ACC-1004",
        "name": "Cobalt on-prem pilot",
        "stage": "Proposal",
        "amount_usd": 150000,
        "close_date": "2026-11-30",
        "next_step": "Scope on-prem deployment requirements with their platform team.",
    },
    "OPP-5005": {
        "id": "OPP-5005",
        "account_id": "ACC-1005",
        "name": "Willow renewal",
        "stage": "Negotiation",
        "amount_usd": 210000,
        "close_date": "2026-07-28",
        "next_step": "Escalate to exec sponsor to unblock budget freeze.",
    },
    "OPP-5006": {
        "id": "OPP-5006",
        "account_id": "ACC-1006",
        "name": "Fernwood tier upgrade",
        "stage": "Discovery",
        "amount_usd": 36000,
        "close_date": "2026-09-25",
        "next_step": "Run usage review to build the upgrade business case.",
    },
    "OPP-5007": {
        "id": "OPP-5007",
        "account_id": "ACC-1007",
        "name": "Summit annual prepay",
        "stage": "Closed Won",
        "amount_usd": 24000,
        "close_date": "2026-06-30",
        "next_step": "Kick off onboarding and schedule admin training.",
    },
}

# ---------------------------------------------------------------------------
# Knowledge base (what `search_knowledge_base` / `read_doc` return)
# ---------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    "DOC-PRICING": {
        "id": "DOC-PRICING",
        "title": "Pricing and packaging",
        "tags": ["pricing", "discount", "packaging"],
        "body": (
            "Standard tiers are Team, Business, and Enterprise. Enterprise includes "
            "SSO, audit logs, and a dedicated success manager. Discounts above 15% "
            "require deal-desk approval. Multi-year commitments unlock up to 20% off."
        ),
    },
    "DOC-SECURITY": {
        "id": "DOC-SECURITY",
        "title": "Security and compliance",
        "tags": ["security", "hipaa", "soc2", "data residency"],
        "body": (
            "We are SOC 2 Type II certified. HIPAA coverage is available on Enterprise "
            "with a signed BAA. EU data residency is supported in the Frankfurt region "
            "for Enterprise customers."
        ),
    },
    "DOC-ONBOARDING": {
        "id": "DOC-ONBOARDING",
        "title": "Customer onboarding",
        "tags": ["onboarding", "implementation", "timeline"],
        "body": (
            "Standard onboarding takes two weeks and includes a kickoff, data import, "
            "and admin training. Enterprise onboarding adds a dedicated implementation "
            "engineer and a custom rollout plan."
        ),
    },
    "DOC-COMPETITORS": {
        "id": "DOC-COMPETITORS",
        "title": "Competitive positioning",
        "tags": ["competitor", "positioning", "differentiation"],
        "body": (
            "Against competitors, lead with our observability depth and faster time to "
            "value. Do not disparage competitors by name. Focus on measurable outcomes "
            "the customer cares about."
        ),
    },
    "DOC-SUPPORT": {
        "id": "DOC-SUPPORT",
        "title": "Support and SLAs",
        "tags": ["support", "sla", "uptime", "escalation"],
        "body": (
            "Business tier includes email support with next-business-day response. "
            "Enterprise adds 24/7 support, a 99.9% uptime SLA, and a named escalation "
            "contact. Sev-1 incidents receive a response within one hour."
        ),
    },
    "DOC-INTEGRATIONS": {
        "id": "DOC-INTEGRATIONS",
        "title": "Integrations and API",
        "tags": ["integration", "api", "webhook", "sdk"],
        "body": (
            "We offer REST and streaming APIs with SDKs for Python and TypeScript. "
            "Prebuilt integrations cover Slack, Salesforce, and common data warehouses. "
            "Webhooks are available on Business and Enterprise tiers."
        ),
    },
    "DOC-DEPLOYMENT": {
        "id": "DOC-DEPLOYMENT",
        "title": "Deployment options",
        "tags": ["deployment", "on-prem", "cloud", "vpc"],
        "body": (
            "The default is multi-tenant cloud. Enterprise customers can opt into a "
            "single-tenant VPC deployment. On-prem deployment is available on a "
            "case-by-case basis and requires a solutions architect review."
        ),
    },
    "DOC-BILLING": {
        "id": "DOC-BILLING",
        "title": "Billing and contracts",
        "tags": ["billing", "invoice", "payment", "contract"],
        "body": (
            "Standard billing is annual upfront by invoice with net-30 terms. Monthly "
            "billing is available on Team and Business tiers. Annual prepay unlocks a "
            "small discount and simplifies procurement for SMB customers."
        ),
    },
}


def find_accounts(query: str) -> list[dict]:
    """Return accounts whose id or name loosely matches the query."""
    q = query.strip().lower()
    return [
        acct
        for acct in ACCOUNTS.values()
        if q in acct["id"].lower() or q in acct["name"].lower()
    ]


def search_docs(query: str) -> list[dict]:
    """Return knowledge base docs matching the query in title, tags, or body."""
    q = query.strip().lower()
    hits = []
    for doc in KNOWLEDGE_BASE.values():
        haystack = " ".join([doc["title"], " ".join(doc["tags"]), doc["body"]]).lower()
        if q in haystack:
            hits.append(doc)
    return hits
