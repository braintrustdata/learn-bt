# 2.1 Instrument the agent with Braintrust tracing

The agent in `agent/` has no tracing yet. Add it three ways, seeding a few traces after
each so you can see how the spans come across.

Seed traces with:

```bash
uv run python -m scripts.seed --count <int>
```

## Task

### 1. Instrument with the CLI and a coding agent

Rather than writing the tracing code by hand, use the Braintrust CLI to drive your
coding agent through the instrumentation. From the repo root, run:

```bash
bt setup instrument --agent <coding-agent> #[claude, codex, cursor, etc.]
```

This downloads the latest `instrument` workflow docs and hands them to the agent,
which then adds tracing to `agent/agent.py` (initializing a logger and enabling
auto-instrumentation so agent runs, model calls, and tool calls are all traced).

Then seed some traces and confirm they appear in your project:

```bash
uv run python -m scripts.seed --count 5
```

Did it work? Open the logs (`bt view logs` or the Braintrust UI) and inspect a trace. 
If the coding agent instrumented correctly, you should see the agent run as the root span, 
with model and tool calls nested underneath, without having written any per-call tracing code yourself.

Now, undo the agent's changes (discard changes from git history). We will now 
explore instrumenting via provider integration.

### 2. Provider wrapping with decorators

The Braintrust SDK provides wrappers integrations for most of the common agent frameworks and model providers. 
Call `setup_pydantic_ai()` at the top level of the agent (`agent/agent.py`).
Seed some traces and look at how they appear.

You should see in the new logs that the entire agent run is automatically captured as a 
trace, including tool calls, in its proper execution heirarchy.

The wrapper also captures attachments. Seed with `--attachment-ratio 0.4` and any file
sent to the model, such as a PDF or image, is logged as an `Attachment` and previews in
the trace, again with no extra code.

### 3. Log a custom span

For custom business logic and functions, we can trace them by adding the `@traced` decorator to
the function. When this decorator is active, Braintrust will automatically capture the input and output
to the function as part of the span. We can customize the span type and name via `type` and `name` parameters
on the decorator. We can also omit the automatic input/output capture by passing `notrace_io=True` to the decorator.
When doing so, we can manually log the span shape by calling `span.log()` to control what gets logged. 

The agent's tool calls are already captured by the provider wrapper, but the business logic
underneath them is not. Those helpers live in `agent/fixtures.py`. Add a `@traced` decorator to
`find_accounts` and `search_docs` so they show up as their own spans, nested under the tool
calls that invoke them. Seed some traces and confirm the new spans appear in the right place.

`search_docs` returns the full matching documents, including their entire bodies, which is more
than you want on the span. Pass `notrace_io=True` to its decorator and call `span.log()` to log a
trimmed output instead, such as the number of hits and the matched document ids, along with the
matched search terms as metadata. Seed some more traces and compare how `search_docs` now logs
against the automatic capture on `find_accounts`.



## Solution

See [01-instrument-tracing.solution.md](01-instrument-tracing.solution.md).
