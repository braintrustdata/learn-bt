# 3.1 Curate a dataset

Turn real agent traces into a focused dataset for one behavior: drafting customer emails. Create a dataset named **email-drafting**. You will use it in the next two exercises.

## Step 1: Add a few traces by hand

Open **learn-bt**, then **Logs**. Filter to traces that contain the **draft_email** tool span:

~~~sql
any_span(span_attributes.name = 'draft_email')
~~~

Open several matching runs. For each good example, select the root span, choose **Add to dataset**, then create or select **email-drafting**.

Choose examples that genuinely test email drafting. This is deliberate curation, not a random export of all traffic.

## Step 2: Use Loop to expand coverage

Open Loop from the Logs page and enter:

~~~text
Find more runs where the agent drafted a customer email. Add good, diverse
examples to the email-drafting dataset.
~~~

Inspect a few rows that Loop adds. Hand curation gives you a high-confidence starting set. Loop can expand coverage without requiring inspection of every trace.

## Step 3: Add the repeatable pipeline

Open **evals/dataset_pipeline.py**. Replace the commented-out template with:

~~~python
from braintrust import DatasetPipeline


async def transform(id=None, input=None, output=None, metadata=None, expected=None, trace=None):
    spans = await trace.get_spans()

    root = next(s for s in spans if s.is_root)
    draft = next(
        s for s in spans if (s.span_attributes or {}).get("name") == "draft_email"
    )

    row_input = {"prompt": root.input["prompt"]}
    attachments = root.input.get("attachments")
    if attachments:
        row_input["attachment"] = attachments[0]

    return {
        "input": row_input,
        "metadata": {"original_reference": draft.output["email"]},
    }


DatasetPipeline(
    name="email-drafting-pipeline",
    source={
        "project_name": "learn-bt",
        "filter": 'any_span(span_attributes.name = "draft_email")',
        "scope": "trace",
    },
    transform=transform,
    target={
        "project_name": "learn-bt",
        "dataset_name": "email-drafting",
    },
)
~~~

The filter selects whole traces that contain an email draft. The transform runs once per trace, keeps the original request compact, preserves a file reference when present, and saves the original email as review context.

## Step 4: Run and inspect it

From the repository root, run:

~~~bash
bt datasets pipeline run evals/dataset_pipeline.py --limit 20 --window 30d --env-file .env
~~~

Open **Datasets**, then **email-drafting**. Confirm that each row has **input.prompt**, optionally has **input.attachment**, and has the original email under **metadata.original_reference**.

## Solution

See [01-curating-datasets.solution.md](01-curating-datasets.solution.md).
