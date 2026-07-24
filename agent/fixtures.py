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
