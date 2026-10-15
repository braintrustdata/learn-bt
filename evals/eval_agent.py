"""Evaluate recipient correctness on crm-recipient-mismatches.

Run with: bt eval evals/eval_agent.py --env-file .env
"""

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


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
