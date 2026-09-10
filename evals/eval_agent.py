"""Eval for the Sales Assistant

Run the agent over the `email-drafting` dataset and grade each drafted
email with the scorers you created. Run with:

    bt eval evals/eval_agent.py

The reference implementation is in
exercises/3-evals/03-executing-an-eval.solution.md.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# Place local imports below here


# def task(input):
#     TODO
#     pass
#
# Eval(
#     PROJECT,
#     experiment_name="email-drafting-eval",
#     data=[],
#     task=task,
#     scores=[valid_email, email_goal_reached], #type: ignore
# )