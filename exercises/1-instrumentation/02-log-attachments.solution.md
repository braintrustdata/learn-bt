# Solution: Log attachments

The change is in `agent/agent.py`. Open a child span for the user message, and log
the prompt and any attachments as that span's input.

```python
from braintrust import Attachment, start_span


def _braintrust_attachment(path: str | Path) -> Attachment:
    p = Path(path)
    media_type = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return Attachment(data=p.read_bytes(), filename=p.name, content_type=media_type)
```

Inside `run_agent`, wrap the run in a child span and log the attachments there:

```python
    user_input: list = [prompt]
    for attachment in attachments or []:
        user_input.append(_load_attachment(attachment))

    with start_span(name="user_message", type="task") as span:
        logged_input = {"prompt": prompt}
        if attachments:
            logged_input["attachments"] = [
                _braintrust_attachment(a) for a in attachments
            ]
        span.log(input=logged_input)

        result = agent.run_sync(user_input)
        span.log(output=result.output)
```

## Notes

- The attachment is logged on the `user_message` child span, not the root, because
  that is the span the file actually belongs to (the user's message). The model
  call spans nest underneath it.
- `Attachment` accepts bytes (as here) or a path via `data="path/to/file"`. The
  SDK uploads it out of band and replaces it with a reference, so images and PDFs
  preview in the trace without bloating the span or slowing down logging.
- Both PNG and PDF attachments from the seed script work the same way; the content
  type is inferred from the file extension.
