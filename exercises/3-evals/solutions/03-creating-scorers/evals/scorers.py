import braintrust
from pydantic import BaseModel

project = braintrust.projects.create(name="learn-bt")


class TraceParams(BaseModel):
    trace: dict


def crm_primary_contact_emails(tool_spans):
    emails = set()
    for span in tool_spans:
        if (span.span_attributes or {}).get("name") != "lookup_customer":
            continue

        accounts = (span.output or {}).get("accounts", [])
        for account in accounts:
            contact = account.get("primary_contact") or {}
            email = contact.get("email")
            if email:
                emails.add(email.strip().casefold())
    return emails


async def recipient_matches_crm(trace=None):
    if not trace:
        return None

    tool_spans = await trace.get_spans(span_type=["tool"])
    draft = next(
        (
            span
            for span in tool_spans
            if (span.span_attributes or {}).get("name") == "draft_email"
        ),
        None,
    )
    if not draft:
        return 0

    recipient = ((draft.output or {}).get("email") or {}).get("recipient", "")
    expected_recipients = crm_primary_contact_emails(tool_spans)
    if not recipient or not expected_recipients:
        return 0

    return int(recipient.strip().casefold() in expected_recipients)


project.scorers.create(
    name="Recipient matches CRM",
    slug="recipient-matches-crm",
    parameters=TraceParams,
    handler=recipient_matches_crm,
)
