# 4.3 Execute an eval

Write an eval that runs the agent over the dataset you curated in 4.1 and scores
it with the scorers you pushed in 4.2.

## Task

1. In `evals/eval_agent.py`, write the eval: load the `sales-assistant-eval`
   dataset, use the agent as the task (each `input` runs through `run_agent`), and
   apply your scorers.
2. Run it and open the experiment:

   ```bash
   bt eval evals/eval_agent.py
   ```

## Solution

See [03-executing-an-eval.solution.md](03-executing-an-eval.solution.md).
