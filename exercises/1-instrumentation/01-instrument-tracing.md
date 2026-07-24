# 2.1 Instrument the agent with Braintrust tracing

The agent in `agent/` has no tracing yet. Add it three ways, seeding traces after
each so you can see how the spans come across.

Seed traces with:

```bash
uv run python -m scripts.seed --count <int>
```

## Task

### 1. Auto-instrumentation
# TODO - Use CLI for instrumentation
At the top level of the invoke in `agent/agent.py`, initialize a logger and call
`braintrust.auto_instrument()`. Seed some traces and look at how they appear.

### 2. Provider wrapping with decorators

Instead of `auto_instrument()`, call `setup_pydantic_ai()` at the top level of the
agent. Add `@traced` decorators to intermediate methods, such as the tool calls in
`agent/tools.py`. Optionally set the span type with `@traced(type="tool")`. Seed
some traces and look at how they appear.

### 3. Log a custom span

On one of the decorated methods, pass `notrace_io=True` to the decorator and call
`span.log()` to manually control what gets logged. Add custom metadata to the
span.

## Solution

See [01-instrument-tracing.solution.md](01-instrument-tracing.solution.md).
