# Solution: Execute an eval

Implementation for `evals/eval_agent.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from braintrust import Eval, init_dataset

from agent.agent import InputFile, run_agent
from scorers import valid_email, email_goal_reached

PROJECT = "learn-bt"
DATASET = "email-drafting"


def task(input):
    attachments = []
    attachment = input.get("attachment")
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return run_agent(input["prompt"], attachments=attachments).output


Eval(
    PROJECT,
    experiment_name="email-drafting-eval",
    data=init_dataset(project=PROJECT, name=DATASET),
    task=task,
    scores=[valid_email, email_goal_reached], #type: ignore
)
```

Run it:

```bash
bt eval evals/eval_agent.py
```

## Notes

- `init_dataset` loads the `email-drafting` dataset from 3.1. Each row's `input`
  (`{"prompt": ...}`) runs through the task.
- `init_dataset` hydrates any
  saved attachment into a `ReadonlyAttachment`, so the task reads its bytes
  (`attachment.data`) and passes an `InputFile` into `run_agent`.
- The task returns `run_agent(...).output`, the agent's final reply. It does not
  need to surface the drafted email: the scorers do that themselves. Because the
  agent is instrumented, each run produces a trace, and `valid_email` and
  `email_goal_reached` filter that trace to the `draft_email` span to grade the
  email (see 3.2).
  the same scorers you pushed in 3.2. Braintrust passes each the run's `trace`.
- Tip: Use `bt eval --first 3 evals/eval_agent.py` for a fast smoke run.
