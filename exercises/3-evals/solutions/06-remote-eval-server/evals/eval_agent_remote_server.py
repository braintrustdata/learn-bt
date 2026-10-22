"""Remote eval server for the Sales Assistant."""

import sys
import uuid
from pathlib import Path

from braintrust import Eval, init_function
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.agent import Agent, InputFile
from agent.config import AgentConfig, DEFAULT_CONFIG

PROJECT = "learn-bt"


class MaxToolCallsParam(BaseModel):
    value: int = Field(
        default=DEFAULT_CONFIG.max_tool_calls,
        description="The most tool calls the agent may make to answer one customer message.",
    )


parameters = {
    "main": {
        "type": "prompt",
        "description": "Agent's main prompt",
        "default": {
            "prompt": {
                "type": "chat",
                "messages": DEFAULT_CONFIG.system_prompt_messages,
            },
            "options": {"model": DEFAULT_CONFIG.model},
        },
    },
    "max_tool_calls": MaxToolCallsParam,
}


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
    parameters=parameters,
)
