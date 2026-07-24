"""Tools for the Sales Assistant agent.

Read tools query the fixtures. Write tools (``draft_email``, ``update_crm_record``)
are mocks: they do not touch any real system, they just record the action and
return a confirmation. That keeps the agent safe to run repeatedly during the
workshop while still exercising the "the model chose to take an action" path.

Each function's signature defines the tool's argument schema. The human-readable
descriptions come from ``config.AgentConfig.tool_descriptions`` so they can be
tuned without editing this file.
"""

from . import fixtures

# Records write-tool calls so a run's side effects can be inspected. Reset per run
# by the agent module. This is a stand-in for actually mutating Salesforce.
WRITE_LOG: list[dict] = []


def lookup_customer(query: str) -> dict:
    """Look up a customer account by id or company name."""
    matches = fixtures.find_accounts(query)
    if not matches:
        return {"found": False, "query": query, "accounts": []}
    return {"found": True, "query": query, "accounts": matches}


def get_opportunity(opportunity_id: str) -> dict:
    """Get a sales opportunity by its id."""
    opp = fixtures.OPPORTUNITIES.get(opportunity_id.strip().upper())
    if opp is None:
        return {"found": False, "opportunity_id": opportunity_id}
    return {"found": True, "opportunity": opp}


def search_knowledge_base(query: str) -> dict:
    """Search the internal knowledge base for relevant docs."""
    hits = fixtures.search_docs(query)
    return {
        "query": query,
        "results": [
            {"id": d["id"], "title": d["title"], "body": d["body"]} for d in hits
        ],
    }


def draft_email(recipient: str, subject: str, body: str) -> dict:
    """Draft an email to a customer contact. Does not send."""
    email = {"recipient": recipient, "subject": subject, "body": body}
    WRITE_LOG.append({"action": "draft_email", "payload": email})
    return {"status": "drafted", "email": email}


def update_crm_record(record_id: str, field: str, value: str) -> dict:
    """Update a field on a CRM account or opportunity record. Mocked."""
    result = {"record_id": record_id, "field": field, "value": value}
    WRITE_LOG.append({"action": "update_crm_record", "payload": result})
    return {"status": "updated", "record": result}


# Maps tool name -> function. The agent builder pairs these with the descriptions
# in the config so both the schema and the wording are explicit.
TOOLS = {
    "lookup_customer": lookup_customer,
    "get_opportunity": get_opportunity,
    "search_knowledge_base": search_knowledge_base,
    "draft_email": draft_email,
    "update_crm_record": update_crm_record,
}
