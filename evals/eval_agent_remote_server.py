"""Remote eval server for the Sales Assistant.

Start with: bt eval evals/eval_agent_remote_server.py --dev --env-file .env
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# TODO: load_parameters(...), write the task that reads hooks.parameters and runs
# the agent, and wire it into Eval(...).
#
# def task(input, hooks):
#     pass
# Eval(
#     PROJECT,
#     data=[],
#     task=task,
#     scores=[recipient_matches_crm, email_quality], #type: ignore
#     parameters=saved_parameters,
# )
