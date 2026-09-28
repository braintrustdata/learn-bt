"""Remote eval server for the Sales Assistant."""

import sys
from pathlib import Path

from braintrust import Eval, load_parameters

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.agent import InputFile, run_agent
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
        max_turns=hooks.parameters["max_turns"],
    )

    attachments = []
    attachment = input.get("attachment")
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return run_agent(input["prompt"], attachments=attachments, config=config).output


Eval(
    PROJECT,
    data=[],
    task=task,
    scores=[recipient_matches_crm],  # type: ignore
    parameters=saved_parameters,
)
