# seed_default

Fills a Braintrust project with Sales Assistant logs by replaying a recorded
snapshot instead of running the agent, so seeding costs no model tokens.

```bash
uv run python -m scripts.seed_default --project my-project
```

Only `BRAINTRUST_API_KEY` is needed. The project is created if it does not exist.

## What is preserved, and what is not

The snapshot holds the full span tree, so a replayed trace is the same trace.

Two things, though, are rewritten:

- **Timestamps.** Every span is shifted by one constant offset that lands the
  newest recorded span at the present moment, so the logs are fresh while
  keeping their positions relative to each other.
- **Attachment keys.** Attachment bytes are keyed per org, so each file is
  re-uploaded into the destination org and its references are rewritten to the
  new key. Each reference keeps its own display filename.

Automation output (Patterns, online scoring) is left out of the snapshot.

## Re-recording the snapshot

`fetch.py` rebuilds `snapshot/` from a live project. Run it when the agent
changes enough that the recorded traces no longer look like what attendees
would produce.

```bash
uv run python -m scripts.seed_default.fetch
uv run python -m scripts.seed_default.fetch --source-project my-project --traces 50
```
