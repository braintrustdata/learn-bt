"""Remote eval server for the Sales Assistant."""

import sys
import uuid
from pathlib import Path

from braintrust import Eval, init_function, load_parameters

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.agent import Agent, InputFile
from agent.config import AgentConfig

PROJECT = "learn-bt"
saved_parameters = load_parameters(project=PROJECT, slug="sales-assistant-parameters")


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


def task(input, hooks):
    prompt_param = hooks.parameters["main"]
    system_prompt_messages = [
        message.as_dict() for message in prompt_param.prompt.messages
    ]

    config = AgentConfig(
        model=prompt_param.options.get("model"),
        system_prompt_messages=system_prompt_messages,
        max_tool_calls=hooks.parameters["max_tool_calls"],
    )

    attachments = []
    attachment = input.get("attachment")
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return Agent(config).chat_turn(
        input["prompt"],
        session_id=uuid.uuid4().hex,
        attachments=attachments,
        history=input.get("history"),
    ).output


Eval(
    PROJECT,
    data=[],
    task=task,
    scores=[recipient_matches_crm, email_quality],  # type: ignore
    parameters=saved_parameters,
)
