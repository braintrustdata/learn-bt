# 3.1 Query logs with filters, SQL, and the CLI [UI + CLI]

First, seed a good volume of logs to query:

```bash
uv run python -m scripts.seed --count 100 --attachment-ratio 0.2 --concurrency 10
```

This may take a couple minutes to complete. Each seeded run is an account executive's request to the sales assistant. Some requests reference a specific opportunity (for example `OPP-5001`, "Northwind EU expansion"), and roughly 20% arrive with an attachment.

## Task

1. **Filter for logs with attachments.** We want to view only logs with attachments to inspect the traces further. In 2.1 you logged a `has_attachments` metadata flag on each run's root span. On the **Logs** page, add a filter that uses it to show only the logs that carried an attachment.

2. **Fuzzy search for one opportunity.** Sometimes, we need to do a fuzzy full text search to filter logs. Use the search box on the Logs page to find the runs about a single opportunity. Search by its name or id (for example "Northwind EU expansion" or `OPP-5001`).

3. **Export a batch of logs for offline analysis.** A teammate wants to review
   the agent's responses offline in a spreadsheet. Go to the **SQL sandbox** and
   write a query against `project_logs` that returns exactly what a reviewer
   needs, one row per run:

   - the time the run happened,
   - the request that came in,
   - the response the agent produced,
   - the tokens it used, and
   - the estimated cost.

   Scope it to the last 7 days, put the most expensive runs first, and return
   one row per trace (not one row per span). Then use the **download** button to
   export the results as CSV.

   The [SQL reference](https://www.braintrust.dev/docs/reference/sql) lists the
   available columns and functions.

4. **Fetch the same data from a coding agent.** Take the query from step 3,
   describe what it should return to a coding agent, and have the agent run it
   against the project with the `bt` CLI.
