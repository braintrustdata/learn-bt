# 2.1 Query logs with filters, SQL, and the CLI [UI + CLI]

This exercise uses the traces you instrumented in Section 1. You will answer the same question with a Logs filter, SQL, and the CLI.

## Step 1: Create enough traffic

From the repository root, use either option.

**Option 1: Generate new traffic**

~~~bash
uv run python -m scripts.seed --count 150 --attachment-ratio 0.2 --concurrency 10
~~~

This creates up to 150 synthetic customer conversations of one to three turns
in your `learn-bt` project. Each customer turn is its own `chat_turn` trace, and
the turns of a conversation share a `metadata.session_id`. A later turn's
`input.history` holds the messages from the earlier turns. About 20% of the conversations include an attachment,
and up to 10 conversations run at once.

This option makes model calls. `scripts.seed` uses `gpt-4o-mini` to generate
each synthetic account-executive request. The Sales Assistant also uses
`gpt-4o-mini` to handle each turn. A turn that uses tools can make more than
one Sales Assistant model call.

**Option 2: Replay the included snapshot**

~~~bash
uv run --env-file .env python -m scripts.seed_default --project learn-bt
~~~

This option does not call a model provider. It replays about 300 recorded `chat_turn`
traces, from 150 conversations of one to three turns, in `scripts/seed_default/snapshot/`. It uploads their attachments
to your Braintrust org, gives the spans current timestamps, and inserts them
into the `learn-bt` project. It still makes Braintrust API calls, but it does
not generate new requests or agent responses.

Each replay adds a new batch of about 300 traces; it does not replace the traffic
already in the project. Run it once for this exercise. If you need to restart,
clear the existing project logs before replaying the snapshot again.

Wait for the command to finish before querying.

![Replayed multi-turn conversations in Braintrust Logs](assets/01-replayed-logs-list.png)

## Step 2: Filter attachment-bearing turns

Open **learn-bt**, then select **Logs**. Add this filter:

~~~sql
metadata.has_attachments = true
~~~

Open a result, which is the `chat_turn` trace for one customer turn.
Its input contains the attachment from Exercise 1.2. The `has_attachments`
field lives on that turn, so you can find attachment-bearing work without
opening every LLM span.

![Attachment-bearing agent turns filtered in Braintrust Logs](assets/02-filter-attachment-runs.png)

## Step 3: Search for one business context

In the Logs search box, enter an opportunity ID or name:

~~~text
OPP-5001
~~~

Or:

~~~text
Northwind EU expansion
~~~

Open a matching `chat_turn` trace and read the request in its input. Search is useful when you know the situation you want to
investigate but did not record it as structured metadata.

![Searching a multi-turn trace for an opportunity ID in Braintrust Logs](assets/03-search-business-context.png)

## Step 4: Export one row per customer turn with SQL

Open the **SQL sandbox**. Start with this query:

~~~sql
SELECT
  created,
  input.prompt AS request,
  output.output AS response,
  metrics.tokens AS tokens,
  metrics.estimated_cost AS estimated_cost
FROM project_logs('learn-bt')
WHERE name = 'chat_turn'
  AND created >= NOW() - INTERVAL 7 DAY
ORDER BY estimated_cost DESC
~~~

Run it, then select **Download** to export a CSV. Each `chat_turn` trace holds
one customer turn's request and response, so a row per trace is a row per
customer turn.

If your input or output has a different shape, inspect one `chat_turn` span and
adjust the fields. The [SQL reference](https://www.braintrust.dev/docs/reference/sql) lists the available columns and functions.

![SQL sandbox query exporting one row per customer turn](assets/04-export-root-runs-sql.png)

## Step 5: Run the same query with the CLI

From the repository root, run:

~~~bash
bt sql --force-ignore-linter "SELECT created, input.prompt AS request, output.output AS response, metrics.tokens AS tokens, metrics.estimated_cost AS estimated_cost FROM project_logs('learn-bt') WHERE name = 'chat_turn' AND created >= NOW() - INTERVAL 7 DAY ORDER BY estimated_cost DESC" --env-file .env
~~~

The CLI reports a sort-planning warning for this query. The explicit flag runs
the workshop query despite that warning.

Compare the terminal result with your CSV. Both should show one row per
customer turn in the same cost order. The UI is useful for exploration. The
CLI is useful in scripts and coding-agent workflows.
