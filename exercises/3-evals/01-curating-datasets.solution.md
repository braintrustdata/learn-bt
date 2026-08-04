# Solution: Curate a dataset

## 1. Curate by hand from the UI

On the **Logs** page, filter to the runs where the agent drafted an email. The
`draft_email` tool call shows up as its own span in the trace, so the filter is a
trace-level `any_span(...)` over the tool span name:

```sql
any_span(span_attributes.name = 'draft_email')
```

Open a few of the matching runs, select the root span, and select "Add to" -> Add to Dataset.

## 2. Curate with Loop

Ask Loop something like: "Find interseting runs where the
agent drafted an email and add them to the `email-drafting` dataset." Loop
resolves the same filter and does the promotion in bulk, which is how you scale
past hand-picking. A coding agent driving `bt` (query logs, then add rows) can do the same job from the terminal.

## 3. Curate with a dataset pipeline

The reference for the pipeline is
[`evals/dataset_pipeline.py`](../../evals/dataset_pipeline.py):

```python
from braintrust import DatasetPipeline

async def transform(id=None, input=None, output=None, metadata=None, expected=None, trace=None):
    spans = await trace.get_spans()

    root = next(s for s in spans if s.is_root)
    draft = next(
        s for s in spans if (s.span_attributes or {}).get("name") == "draft_email"
    )

    row_input = {"prompt": root.input["prompt"]}

    # If the run had an attachment, preserve it as a reference in the dataset too.
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
```

Run it:

```bash
bt datasets pipeline run evals/dataset_pipeline.py --limit 20 --window 30d
```

## Notes

- **The filter selects whole traces.** `any_span(span_attributes.name =
  'draft_email')` keeps a trace if any of its spans is a `draft_email` call, and
  `scope: "trace"` makes each matching trace a single source, so the transform
  runs once per run rather than once per span.
- **The pipeline is code.** Unlike clicking **Add to dataset** or asking Loop, it is version-controlled, reviewable, and repeatable: rerun it to pull in new email-drafting traces as more traffic arrives.
- For larger jobs, split the run into `pull` / `transform` / `push` stages so you can inspect the rows in `bt-sync/transformed.jsonl` before writing them.
