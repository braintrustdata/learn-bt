"""Eval for the Sales Assistant."""

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from braintrust import Eval, init_dataset

from agent.agent import Agent, InputFile
from scorers import email_quality, recipient_matches_crm

PROJECT = "learn-bt"
DATASET = "crm-recipient-mismatches"


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
