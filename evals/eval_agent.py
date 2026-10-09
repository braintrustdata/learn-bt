"""Eval recipient correctness for the Sales Assistant.

Run the agent over the `crm-recipient-mismatches` regression dataset and grade
whether each new email draft uses the CRM primary-contact address. Run with:

    bt eval evals/eval_agent.py

The completed source is in
exercises/3-evals/solutions/04-executing-an-eval/evals/eval_agent.py.
"""

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# Place local imports below here


# def task(input):
#     TODO
#     pass
#
# Eval(
#     PROJECT,
#     experiment_name="recipient-mismatch-baseline",
#     data=[],
#     task=task,
#     scores=[recipient_matches_crm, email_quality],  # type: ignore
# )
