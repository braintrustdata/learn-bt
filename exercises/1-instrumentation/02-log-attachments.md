# 2.2 Log attachments

Requests sometimes arrive with a file (a forwarded email, an RFP, a screenshot).
Log that file as a Braintrust `Attachment`. This uploads the attachment to Braintrust
and renders cleanly in the trace view. There are other ways to reference attachments, 
however, such as external attachments or images. See more details [here](https://www.braintrust.dev/docs/annotate/datasets/create#multimodal-datasets)
Seed some attachment-bearing traces (the seed script produces both images and
PDFs):

```bash
uv run python -m scripts.seed --count 10 --attachment-ratio 0.4
```

## Task
Currently, we are not logging the attachments that our agent handles.

In `agent/agent.py`, when `run_agent` is called with attachments, wrap each file
in a Braintrust `Attachment` and log it as the input of the child span that
represents the user message.

## Solution

See [02-log-attachments.solution.md](02-log-attachments.solution.md).
