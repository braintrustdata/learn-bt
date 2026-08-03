"""Tools for the Sales Assistant agent.

Read tools query the fixtures. Write tools (``draft_email``, ``update_crm_record``)
are mocks.
"""

from __future__ import annotations

import inspect
from typing import Callable

from openai import pydantic_function_tool
from openai.types.chat import ChatCompletionFunctionToolParam
from pydantic import BaseModel, Field, ValidationError

from . import fixtures


class LookupCustomer(BaseModel):
    query: str = Field(description="An account id, such as ACC-1001, or a company name.")


def lookup_customer(query: str) -> dict:
    """Look up a customer account in the CRM by account id or by company name. Returns account details including the primary contact, tier, renewal date,
    and ARR.
    """
    matches = fixtures.find_accounts(query)
    if not matches:
        return {"found": False, "query": query, "accounts": []}
    return {"found": True, "query": query, "accounts": matches}


class GetOpportunity(BaseModel):
    opportunity_id: str = Field(description="An opportunity id, such as OPP-5001.")


def get_opportunity(opportunity_id: str) -> dict:
    """Get the details of a sales opportunity by its id. Returns its stage, amount, close date, and next step.
    """
    opp = fixtures.OPPORTUNITIES.get(opportunity_id.strip().upper())
    if opp is None:
        return {"found": False, "opportunity_id": opportunity_id}
    return {"found": True, "opportunity": opp}


class SearchKnowledgeBase(BaseModel):
    query: str = Field(description="The search terms to look for.")


def search_knowledge_base(query: str) -> dict:
    """Search the internal knowledge base for pricing, security, onboarding, and
    competitive positioning information. Use this before making factual claims about the product.
    """
    hits = fixtures.search_docs(query)
    return {
        "query": query,
        "results": [
            {"id": d["id"], "title": d["title"], "body": d["body"]} for d in hits
        ],
    }


class DraftEmail(BaseModel):
    recipient: str = Field(description="The email address of the customer contact.")
    subject: str = Field(description="The subject line.")
    body: str = Field(description="The body of the email.")


def draft_email(recipient: str, subject: str, body: str) -> dict:
    """Draft an email to a customer contact. Returns the drafted email for review; it is not sent automatically.
    """
    email = {"recipient": recipient, "subject": subject, "body": body}
    return {"status": "drafted", "email": email}


class UpdateCrmRecord(BaseModel):
    record_id: str = Field(description="The id of the account or opportunity to update.")
    field: str = Field(description="The name of the field to update.")
    value: str = Field(description="The new value for the field.")


def update_crm_record(record_id: str, field: str, value: str) -> dict:
    """Update a field on a CRM account or opportunity record. Mocked."""
    result = {"record_id": record_id, "field": field, "value": value}
    return {"status": "updated", "record": result}


#Tool registry used to generate tool specs
TOOLS: dict[str, tuple[type[BaseModel], Callable[..., dict]]] = {
    "lookup_customer": (LookupCustomer, lookup_customer),
    "get_opportunity": (GetOpportunity, get_opportunity),
    "search_knowledge_base": (SearchKnowledgeBase, search_knowledge_base),
    "draft_email": (DraftEmail, draft_email),
    "update_crm_record": (UpdateCrmRecord, update_crm_record),
}


def tool_specs() -> list[ChatCompletionFunctionToolParam]:
    """Build the ``tools`` payload for the Chat Completions API."""
    return [
        pydantic_function_tool(args_model, name=name, description=inspect.getdoc(fn))
        for name, (args_model, fn) in TOOLS.items()
    ]


def dispatch(name: str, arguments: str) -> dict:
    """Run the named tool against a JSON string of arguments from the model."""
    entry = TOOLS.get(name)
    if entry is None:
        return {"error": f"Unknown tool {name!r}. Available tools: {sorted(TOOLS)}."}

    args_model, fn = entry
    try:
        args = args_model.model_validate_json(arguments)
    except ValidationError as exc:
        return {"error": f"Invalid arguments for {name}: {exc}"}

    try:
        return fn(**args.model_dump())
    except Exception as exc:
        return {"error": f"{name} failed: {type(exc).__name__}: {exc}"}
