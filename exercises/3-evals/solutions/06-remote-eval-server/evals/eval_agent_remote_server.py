"""Remote eval server for the Sales Assistant."""

import sys
import uuid
from pathlib import Path

from braintrust import Eval, load_parameters

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.agent import Agent, InputFile
from agent.config import AgentConfig
from scorers import recipient_matches_crm

PROJECT = "learn-bt"
saved_parameters = load_parameters(project=PROJECT, slug="sales-assistant-parameters")


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
        input["prompt"], session_id=uuid.uuid4().hex, attachments=attachments
    ).output


Eval(
    PROJECT,
    data=[],
    task=task,
    scores=[recipient_matches_crm],  # type: ignore
    parameters=saved_parameters,
)
