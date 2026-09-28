"""Remote eval server for the Sales Assistant.

Load the saved parameters (parameters.py) and pass their values down through the
`hooks` object to build an AgentConfig and run the agent. Start the dev server:

    bt eval evals/eval_remote_agent.py --dev

The completed source is in
exercises/4-human-review/solutions/03-remote-eval-server/evals/eval_agent_remote_server.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# Place local imports below here

# TODO: load_parameters(...), write the task that reads hooks.parameters and runs
# the agent, and wire it into Eval(...).
#
# def task(input, hooks):
#     pass
# Eval(
#     PROJECT,
#     data=[],
#     task=task,
#     scores=[recipient_matches_crm], #type: ignore
#     parameters=saved_parameters,
# )
