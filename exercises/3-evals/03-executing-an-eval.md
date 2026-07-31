# 4.3 Execute an eval

Put the last two exercises together: run the agent over the `email-drafting`
dataset from 4.1 and grade each drafted email with the scorers from 4.2.

## Task

1. In [`evals/eval_agent.py`](../../evals/eval_agent.py), build the `Eval`: load
   the `email-drafting` dataset, run `run_agent` on each row's `prompt` as the
   task, and pass `valid_email` and `email_goal_reached` as the scores. Note, our agent also needs to handle attachments sometimes. 
2. Run it and open the experiment:

   ```bash
   bt eval evals/eval_agent.py
   ```

## Solution

See [03-executing-an-eval.solution.md](03-executing-an-eval.solution.md).
