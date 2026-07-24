# Solution: Execute an eval

Implementation for `evals/eval_agent.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from braintrust import Eval, init_dataset
from autoevals import Factuality

from agent.agent import run_agent

PROJECT = "sales-assistant"
DATASET = "sales-assistant-eval"


def task(input: str) -> str:
    return run_agent(input).output


Eval(
    PROJECT,
    data=init_dataset(project=PROJECT, name=DATASET),
    task=task,
    scores=[Factuality()],
    experiment_name="sales-assistant-baseline",
)
```

Run it:

```bash
bt eval evals/eval_agent.py
```

## Notes

- `init_dataset` loads the dataset from 4.1. Each row's `input` runs through the
  task and its `expected` is available to scorers.
- `task` is the agent itself. Because the agent is instrumented, each eval row
  also produces a full trace under the experiment, so you can open any row and see
  the tool calls behind its score.
- `Factuality` is an autoevals judge. Add the scorers you pushed in 4.2 to the
  experiment from the UI, or import and pass them in `scores` directly.
- To compare versions, change `agent/config.py` (for example the model, which the
  gateway makes a one-line swap), give the run a new `experiment_name`, and re-run.
  Select both experiments in the UI to see the diff.
- Use `bt eval --first 3 evals/eval_agent.py` for a fast smoke run while iterating.
