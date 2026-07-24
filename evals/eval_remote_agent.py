"""Remote eval server for the Sales Assistant (exercise 5.3, part 2).

Load the saved parameters (parameters.py) and pass their values down through the
`hooks` object to build an AgentConfig and run the agent. Start the dev server:

    bt eval evals/eval_remote_agent.py --dev

The reference implementation is in
exercises/4-human-review/03-remote-eval-server.solution.md.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# TODO: load_parameters(...), write the task that reads hooks.parameters and runs
# the agent, and wire it into Eval(...).
