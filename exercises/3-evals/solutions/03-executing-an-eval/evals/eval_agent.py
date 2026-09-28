"""Eval for the Sales Assistant."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from braintrust import Eval, init_dataset

from agent.agent import InputFile, run_agent
from scorers import recipient_matches_crm

PROJECT = "learn-bt"
DATASET = "crm-recipient-mismatches"


def task(input):
    attachments = []
    attachment = input.get("attachment")
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return run_agent(
        input["prompt"],
        attachments=attachments,
        history=input.get("history"),
    ).output


Eval(
    PROJECT,
    experiment_name="recipient-mismatch-baseline",
    data=init_dataset(project=PROJECT, name=DATASET),
    task=task,
    scores=[recipient_matches_crm],  # type: ignore
)
