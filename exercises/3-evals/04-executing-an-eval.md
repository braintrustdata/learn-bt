# 3.4 Establish the recipient-mismatch baseline

In Module 2, we used active observability to identify recurring issues,
including emails sent to the wrong recipient. Now we turn those confirmed
failures into a fixed test set and measure how reliably the current agent
selects the CRM email when it reruns the same requests. This establishes a
baseline that we can compare against after making the fix.

Open **evals/eval_agent.py**.

## Step 1: Add imports and constants

Below the path setup, add:

~~~python
from braintrust import Eval, init_dataset

from agent.agent import Agent, InputFile
from scorers import email_quality, recipient_matches_crm

PROJECT = "learn-bt"
DATASET = "crm-recipient-mismatches"
~~~

## Step 2: Define the task

Replace the commented-out task template with:

~~~python
def task(input):
    attachments = []
    attachment = input.get("attachment")
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return Agent().chat_turn(
        input["prompt"],
        session_id=uuid.uuid4().hex,
        attachments=attachments,
        history=input.get("history"),
    ).output
~~~

Before an eval row runs, its saved attachment is restored. Each row also passes
the agent the original request and, when needed, `input.history`, which contains
the messages from earlier in the conversation. This gives the agent the context
it had before the failed turn. It does not reuse the email from the original
trace. Instead, it runs again and produces a new draft for the scorer to
evaluate.

## Step 3: Define the eval

Replace the commented-out **Eval** template with:

~~~python
Eval(
    PROJECT,
    experiment_name="recipient-mismatch-baseline",
    data=init_dataset(project=PROJECT, name=DATASET),
    task=task,
    scores=[recipient_matches_crm, email_quality],  # type: ignore
)
~~~

The `recipient_matches_crm` scorer reads the trace from this new eval run, not
the original trace. It returns **1** when the new draft uses a primary-contact
email from that run's CRM lookup. Otherwise, it returns **0**.

The experiment also runs the **email_quality** scorer on the same new draft. Its
explanations can flag writing issues such as placeholders, excessive length, or
tone.

## Step 4: Run the baseline

From the repository root, run the full dataset:

~~~bash
bt eval evals/eval_agent.py --env-file .env
~~~

When the run finishes, open **Experiments** in Braintrust and select
**recipient-mismatch-baseline**. An experiment is a saved record of one eval
run. It keeps the dataset rows, new agent outputs, traces, and scorer results
together so you can inspect and compare them later.

Find the **recipient_matches_crm** score column and look at its average. Every
row was selected from a prior recipient mismatch, and we have not changed the
agent yet, so the score should be low, often close to **0** (or 0%). Some rows may pass
on a particular rerun because model outputs can vary. Open a passing row's new
trace to understand why, but keep every row in the frozen regression dataset.
Use this recorded baseline score to compare the fixed version in the next
exercise.

![Recipient-mismatch baseline experiment results](assets/04-recipient-mismatch-baseline-experiment.png)

## Answer key

Compare your completed [evals/eval_agent.py](solutions/04-executing-an-eval/evals/eval_agent.py)
with this answer key.
