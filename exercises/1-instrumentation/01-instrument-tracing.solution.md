# Solution: Instrument the agent with Braintrust tracing

All changes are in `agent/agent.py` and `agent/tools.py`.

## 1. Auto-instrumentation

At the top of `agent/agent.py`:

```python
import braintrust

braintrust.init_logger(project="sales-assistant")
braintrust.auto_instrument()
```

`auto_instrument()` patches Pydantic AI (and other supported libraries), so agent
runs, model calls, and tool calls are traced with no per-call code.

## 2. Provider wrapping with decorators

Swap `auto_instrument()` for the Pydantic AI wrapper, at the top of
`agent/agent.py`:

```python
from braintrust.wrappers.pydantic_ai import setup_pydantic_ai

setup_pydantic_ai(project_name="sales-assistant")
```

Then decorate the tool functions in `agent/tools.py`:

```python
from braintrust import traced

@traced(type="tool")
def lookup_customer(query: str) -> dict:
    ...
```

`setup_pydantic_ai()` instruments only Pydantic AI (rather than every library).
The `@traced` decorators add your own spans for the tool calls, and `type="tool"`
labels them so they render as tool spans in the trace view.

## 3. Log a custom span

Take one decorated tool, turn off automatic IO logging, and log manually:

```python
from braintrust import current_span, traced

@traced(type="tool", notrace_io=True)
def lookup_customer(query: str) -> dict:
    result = fixtures.find_accounts(query)
    current_span().log(
        input={"query": query},
        output={"num_matches": len(result)},
        metadata={"source": "sfdc", "matched": bool(result)},
    )
    return {"found": bool(result), "query": query, "accounts": result}
```

`notrace_io=True` stops the decorator from auto-logging the function arguments and
return value, so `span.log()` is fully in control of what the span records. This
is how you redact or reshape what gets logged, and attach custom metadata.
