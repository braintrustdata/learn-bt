# Solution: Instrument the agent with Braintrust tracing

All changes are in `agent/agent.py` and `agent/tools.py`.

## 1. Instrument with the CLI and a coding agent

Run the instrumentation flow from the repo root:

```bash
bt setup instrument --agent claude
```

`bt setup instrument` downloads the latest `instrument` workflow docs and runs your
coding agent against them. Following those docs, the agent should add tracing at the top
of `agent/agent.py`, roughly:

```python
import braintrust

braintrust.init_logger(project="sales-assistant")
braintrust.auto_instrument()
```

`auto_instrument()` patches Pydantic AI (and other supported libraries), so agent
runs, model calls, and tool calls are traced with no per-call code.

Often, we need more granularity than what auto_instrument provides, hence, we explore
provider wrapping and custom logging below.

## 2. Provider wrapping

Call `setup_pydantic_ai()` at the top of `agent/agent.py`:

```python
from braintrust import setup_pydantic_ai

setup_pydantic_ai(project_name="learn-bt")
```

`setup_pydantic_ai()` instruments only Pydantic AI (rather than every library).

## 3. Log a custom span

The tool calls are already captured by the provider wrapper, but the business logic
underneath them is not. Those helpers live in `agent/fixtures.py`. Decorate them with
`@traced` so they show up as their own spans, nested under the tool calls that invoke them.

Start with automatic IO capture on `find_accounts`:

```python
from braintrust import traced

@traced
def find_accounts(query: str) -> list[dict]:
    ...
```

The decorator logs the function arguments and return value for you, so the span records the
query in and the matched accounts out with no extra code.

`search_docs` returns the full matching documents, including their entire bodies, which is more
than you want on the span. Turn off automatic IO capture with `notrace_io=True` and log a trimmed
shape manually:

```python
import re

from braintrust import current_span, traced

@traced(notrace_io=True)
def search_docs(query: str) -> list[dict]:
    stopwords = {...}
    terms = [
        t for t in re.findall(r"[a-z0-9]+", query.lower())
        if len(t) >= 3 and t not in stopwords
    ]
    hits = []
    for doc in KNOWLEDGE_BASE.values():
        words = set(re.findall(
            r"[a-z0-9]+",
            " ".join([doc["title"], " ".join(doc["tags"]), doc["body"]]).lower(),
        ))
        if any(term in words for term in terms):
            hits.append(doc)
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
