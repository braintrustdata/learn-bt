# 2.1 Instrument the agent with Braintrust tracing

The agent in `agent/` has no tracing yet. Add it three ways, seeding a few traces after
each so you can see how the spans come across.

Seed traces with:

```bash
uv run python -m scripts.seed --count <int>
```

## Task

### 1. Instrument with the CLI and a coding agent

Rather than writing the tracing code by hand, use the Braintrust CLI to drive your coding agent through the instrumentation. Note: before you do this, make sure to have initialized a git repo so agent changes can be safely discarded.From the repo root, run:

```bash
bt setup instrument --agent <coding-agent> #[claude, codex, cursor, etc.]
```

This downloads the latest `instrument` workflow docs and hands them to the coding agent, which then uses its reasoning/judgement to instrument the Sales Assistant.

Then seed some traces and confirm they appear in your project:

```bash
uv run python -m scripts.seed --count 5
```

Did it work? Open the logs (`bt view logs` or the Braintrust UI) and inspect a trace. 
If the coding agent instrumented correctly, you should see the agent run as the root span, 
with model and tool calls nested underneath, without having written any per-call tracing code yourself.

Now, undo the coding agent's changes (discard changes from git history). We will now 
explore instrumenting via provider integration.

### 2. Provider wrapping and traced functions

The Braintrust SDK provides wrapper integrations for most of the common agent frameworks
and model providers. Our agent calls the OpenAI client directly, so wrap that client with
`wrap_openai()` where it is built in `agent/agent.py`. You also need somewhere for the
spans to go, so call `init_logger()` at the top level of the module.

Seed some traces and look at how they appear. Every model call the agent makes is now an
`llm` span, with metrics automatically parsed.

The wrapper also captures attachments. Seed with `--attachment-ratio 1.0` and any file
sent to the model, such as a PDF or image, is logged as an `Attachment` and previews in
the trace, again with no extra code.

What this doesn't give us is the trace structure. An agent run is several different steps, and logically we want to associate these all with a single trace. A trace should be a unique agent run. We can trace all of the intermediate functions and tool calls via the `@traced` decorator. This decorator automatically captures input and output of the decorated function as a span, and nests the span in its proper trace heirarchy. Pass `type` and `name` parameters to the decorator to control how the span appears:

- `run_agent` in `agent/agent.py` is the root span of a run. Give it `type="task"` and
  `name="agent_run"`.
- each tool function in `agent/tools.py` gets `type="tool"`.
- the business logic functions (`find_accounts()` and `search_docs()`) in `agent/fixtures.py`

Seed again. Spans nest by execution, so each trace should now be one `agent_run` root span
with the model and tool calls underneath it, in the order the agent made them.

### 3. Log a custom span

`@traced` auto captures a function's arguments and return value. Often This is helpful for most scenarios, but sometimes we want to control what gets logged more granularly, or add additional metdata to the sapn.
an extra field, or less than the full input and output. We can achieve this via the `current_span().log()` method. This method manaully logs additional, arbitrary data on the currently active span. This gets merged with anything else that's already captured on the span.

We want to be able to easily denote agent runs that work with attachments. In `run_agent()` log a metadata field called `has_attachments : bool` that is `True` if the agent run is working with attachments.

We can also prevent `@traced` from auto capturing the input and output.
`search_docs` currently returns the full matching documents, including their entire bodies, which is more than you want on the span. Pass `notrace_io=True` to its decorator and call `current_span().log()` to log a trimmed output instead, such as the number of hits and the matched document ids, along with the matched search terms as metadata. Seed some more traces and compare how `search_docs` now logs against the automatic capture on `find_accounts`.



## Solution

See [01-instrument-tracing.solution.md](01-instrument-tracing.solution.md).
