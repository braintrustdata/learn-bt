# Solution: Instrument the agent with Braintrust tracing

All changes are in `agent/agent.py`, `agent/tools.py`, and `agent/fixtures.py`.

## 1. Instrument with the CLI and a coding agent

Run the instrumentation flow from the repo root:

```bash
bt setup instrument --agent claude
```

`bt setup instrument` downloads the latest `instrument` workflow docs and runs your
coding agent against them. Following those docs, the agent should initialize a logger
and add spans for the agent run, the model calls, and the tool calls.

Often, we need more granularity than what a coding agent picks on its own, hence we
explore provider wrapping and custom logging below.

## 2. Provider wrapping and traced functions

In `agent/agent.py`, initialize a logger and wrap the client where it is built:

```python
import braintrust
from braintrust import traced, wrap_openai

braintrust.init_logger(project="learn-bt")


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return wrap_openai(OpenAI(...))
```

`wrap_openai` patches the client instance you hand it, so every
`chat.completions.create` call on it becomes an `llm` span. Only that instance is
affected, which is why the separate client `scripts/seed.py` uses to generate requests
stays out of your logs.

Then the root span:

```python
@traced(type="task", name="agent_run")
def run_agent(prompt, attachments=None, config=DEFAULT_CONFIG) -> AgentResult:
    ...
```

and each tool in `agent/tools.py`:

```python
from braintrust import traced


@traced(type="tool")
def lookup_customer(query: str) -> dict:
    ...
```

Without `name`, a span takes the name of the function it decorates, so the tools need
only `type`. Nesting needs no wiring: the model calls and the tools run inside
`run_agent`, so their spans attach to its span.

## 3. Log a custom span

### A metadata flag on the root span

```python
from braintrust import current_span, traced


@traced(type="task", name="agent_run")
def run_agent(prompt, attachments=None, config=DEFAULT_CONFIG) -> AgentResult:
    current_span().log(metadata={"has_attachments": bool(attachments)})
    ...
```

`current_span()` returns the span `@traced` opened, and `log()` merges into it, so the
input and output are still captured automatically.

### Trimming what gets captured

`search_docs` returns the full matching documents, including their entire bodies, which is more
than you want on the span. Turn off automatic IO capture with `notrace_io=True` and log a trimmed
shape manually:

```python
import re

from braintrust import current_span, traced


@traced(notrace_io=True)
def search_docs(query: str) -> list[dict]:
    #{...function logic}
    
    current_span().log(
        input={"query": query},
        output={"num_hits": len(hits), "doc_ids": [d["id"] for d in hits]},
        metadata={"matched_terms": terms},
    )
    return hits
```

`notrace_io=True` stops the decorator from auto-logging the function arguments and return value,
so `span.log()` is fully in control of what the span records. This is how you redact or reshape
what gets logged, and attach custom metadata. Comparing the two spans in the trace, `find_accounts`
shows its raw IO while `search_docs` shows only the trimmed output and matched terms you chose.
