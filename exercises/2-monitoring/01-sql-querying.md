# 3.1 Query logs with filters, SQL, and the CLI [UI + CLI]

First, seed a good volume of logs to query:

```bash
uv run python -m scripts.seed --count 100 --attachment-ratio 0.3
```

## Task

1. On the **Logs** page, apply a filter directly in the UI, for example to show
   only logs that have attachments.
2. Go to the **SQL sandbox** and write a fully custom SQL query against
   `project_logs`. Come up with the query yourself. The
   [SQL reference](https://www.braintrust.dev/docs/reference/sql) lists the
   available columns and functions.
3. Take that same query, describe what it should return to a coding agent, and
   have the agent execute it against the project through the `bt` CLI.
