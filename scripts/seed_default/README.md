# seed_default

Fills a Braintrust project with Sales Assistant logs by replaying a recorded
snapshot instead of running the agent, so seeding makes no model calls.

```bash
uv run python -m scripts.seed_default --project my-project
```

Only `BRAINTRUST_API_KEY` is needed. The project is created if it does not exist.

## What is preserved, and what is not

The snapshot holds 150 two-turn conversation traces. Each trace has a
`conversation` root and two nested `agent_run` spans, so a replayed trace has
the same structure as a freshly seeded multi-turn conversation.

Two things, though, are rewritten:

- **Timestamps.** Every span is shifted by one constant offset that lands the
  newest recorded span at the present moment, so the logs are fresh while
  keeping their positions relative to each other.
- **Attachment keys.** Attachment bytes are keyed per org, so each file is
  re-uploaded into the destination org and its references are rewritten to the
  new key. Each reference keeps its own display filename.
- **Log IDs.** Each replay creates new log, span, and trace identifiers. This
  keeps a replay valid after the project’s previous logs have been deleted.
  Replaying twice creates two separate batches of traces.

Automation output, including patterns and online scoring, is left out of the
snapshot.

## Re-recording the snapshot

`fetch.py` rebuilds `snapshot/` from a live project. Run it when the agent
changes enough that the recorded traces no longer look like what attendees
would produce. It records the most recent 150 `conversation` roots by default.

```bash
uv run python -m scripts.seed --count 150 --conversation-turns 2 --concurrency 10
uv run python -m scripts.seed_default.fetch --source-project my-project --traces 150
```
