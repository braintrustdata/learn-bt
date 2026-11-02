"""Eval for the Sales Assistant."""

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from braintrust import Eval, init_dataset, init_function

from agent.agent import Agent, InputFile

PROJECT = "learn-bt"
DATASET = "crm-recipient-mismatches"


recipient_matches_crm = init_function(PROJECT, "recipient-matches-crm")
email_quality_scorer = init_function(PROJECT, "email-quality")


async def email_quality(trace, **kwargs):
    tool_spans = await trace.get_spans(span_type=["tool"])
    draft = next(
        (
            span for span in tool_spans
            if span.span_attributes["name"] == "draft_email"
        ),
        None,
    )
    if not draft:
        return None

    return email_quality_scorer(output=draft.output["email"])


def task(input):
    attachments = []
    attachment = input.get("attachment")
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return Agent().chat_turn(
        input["prompt"],
        session_id=uuid.uuid4().hex,
        attachments=attachments,
        history=input.get("history"),
    ).output


Eval(
    PROJECT,
    experiment_name="recipient-mismatch-baseline",
    data=init_dataset(project=PROJECT, name=DATASET),
    task=task,
    scores=[recipient_matches_crm, email_quality],  # type: ignore
)
