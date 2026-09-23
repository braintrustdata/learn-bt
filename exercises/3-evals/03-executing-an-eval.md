# 3.3 Execute an eval

Run the Sales Assistant against the **email-drafting** dataset and score each run with the scorers from Exercise 3.2. The result is an experiment you can inspect and compare when you improve the agent.

Open **evals/eval_agent.py**.

## Step 1: Add imports and constants

Below the path setup, add:

~~~python
from braintrust import Eval, init_dataset

from agent.agent import InputFile, run_agent
from scorers import email_goal_reached, valid_email

PROJECT = "learn-bt"
DATASET = "email-drafting"
~~~

## Step 2: Define the task

Replace the commented-out task template with:

~~~python
def task(input):
    attachments = []
    attachment = input.get("attachment")
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return run_agent(input["prompt"], attachments=attachments).output
~~~

A dataset attachment is hydrated before the task runs. Converting it to **InputFile** exercises the same multimodal path as the production trace that created the row.

## Step 3: Define the eval

Replace the commented-out **Eval** template with:

~~~python
Eval(
    PROJECT,
    experiment_name="email-drafting-eval",
    data=init_dataset(project=PROJECT, name=DATASET),
    task=task,
    scores=[valid_email, email_goal_reached],  # type: ignore
)
~~~

## Step 4: Run and inspect it

From the repository root, run:

~~~bash
bt eval evals/eval_agent.py --env-file .env
~~~

For a fast smoke test, run three rows:

~~~bash
bt eval --first 3 evals/eval_agent.py --env-file .env
~~~

Open the **email-drafting-eval** experiment in Braintrust. Inspect one row with each scorer, then follow its trace to **draft_email**. This verifies that the dataset, task, and trace-aware scorers are connected.

## Solution

See [03-executing-an-eval.solution.md](03-executing-an-eval.solution.md).
