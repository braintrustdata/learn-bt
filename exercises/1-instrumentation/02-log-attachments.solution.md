# Solution: Log attachments

In `agent/agent.py`, extend the `current_span().log()` call:

```python
from braintrust import Attachment, current_span, traced


@traced(type="task", name="agent_run")
def run_agent(prompt, attachments=None, config=DEFAULT_CONFIG) -> AgentResult:
    input_files = [...]

    current_span().log(
        input={
            "attachments": [
                Attachment(data=f.data, filename=f.filename, content_type=f.media_type)
                for f in input_files
            ]
        },
        metadata={"has_attachments": bool(attachments)},
    )
```

`run_agent` normalizes file paths and dataset attachments into `InputFile` before this
point, so one branch covers both.

`@traced` captures the `attachments` argument as whatever was passed, usually a file
path. Logging under the same key replaces that value, so the span ends up with the
uploaded file instead.
