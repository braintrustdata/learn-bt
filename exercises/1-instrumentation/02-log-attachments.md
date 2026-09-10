# 1.2 Log attachments

`wrap_openai` auto captures attachments on the `llm` span, nested inside the messages sent to the model. We can also log attachments manually using the Braintrust SDK. Here, it would be helpful to have the attachments logged on the root span (`run_agent()`) so that some workflows can be simplified, such as adding to logs to a dataset later.

## Task

The `Attachment` class takes a file path or raw bytes plus a filename and content type, and uploads the file to the attachment store.

In `run_agent`, log the run's attachments to the root span's input as `Attachment`
objects.

Seed with `--attachment-ratio 1.0` and open a trace. The root span input should now show
a previewable file rather than the path it was read from.

## Solution

See [02-log-attachments.solution.md](02-log-attachments.solution.md).
