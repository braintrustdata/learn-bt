# Solution: Query logs with filters, SQL, and the CLI

## 1. Filter for logs with attachments

The flag from 2.1 is on the root span, which is the row the Logs table shows, so the
filter reads straight off it:
```sql
metadata.has_attachments = true
```
Alternatively, you can generate this filter by asking Loop in the filter modal.

The attachment itself lives on the `llm` span, nested inside the messages sent to the
model. Filtering on that payload directly would mean matching a path whose position
shifts with the number of turns and content parts, which is exactly why 2.1 tags the run
with a flag instead.

## 2. Fuzzy search for one opportunity

Type the opportunity into the search box, for example `Northwind EU expansion`
or `OPP-5001`. Search is unstructured full text search. 

## 3. Export a batch of logs for offline analysis

In the **SQL sandbox**:

```sql
SELECT
  created,
  input,
  output,
  metrics.tokens AS tokens,
  estimated_cost() AS cost
FROM project_logs
WHERE created >= now() - INTERVAL 7 DAY
  AND span_attributes.name = 'agent_run'
ORDER BY cost DESC
LIMIT 100
```

Then click the **download** button above the results and choose CSV.


## 4. Fetch the same data from a coding agent

Describe the query to a coding agent and have it run the same SQL through the
`bt` CLI. The CLI supports a `sql` command that allows the coding agent to execute arbitrary SQL against Brainstore, effectively running the same query to fetch the same data. This allows for powerful agentic workflows that enables coding agents to take full advantage of Braintrust, without having to access the UI.

## Notes

- The SQL sandbox and Loop run in strict lint mode, which is why the query keeps
  a range filter on `created` and a `LIMIT`. The CLI enforces the same linter;
  pass `--force-ignore-linter` only for a query that is already selective and
  bounded.
