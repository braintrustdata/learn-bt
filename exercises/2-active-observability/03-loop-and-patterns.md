# 2.3 Discover recurring failures with Loop and Patterns

Use instrumented Sales Assistant traffic to investigate whether the agent
completes AE requests correctly.

Start with a question in Loop, turn a supported recurring behavior into a Pattern, then
inspect the Pattern's evidence in the trace itself.

## Step 1: Discover candidate failures

Open **learn-bt**, then select **Loop** in the project sidebar. Start a new
thread and ask:

~~~text
Review the current Sales Assistant logs. Identify up to three recurring behaviors or possible failure modes. For each one, link the supporting traces, explain the evidence, and say whether it is worth tracking.
~~~

Inspect the trace links in Loop's response. Loop's response will also create and link to Patterns, which we'll explain in the next step.

![Loop groups findings from Sales Assistant logs into reported Patterns.](assets/02-loop-investigation-and-reported-patterns.png)

## Step 2: Read a Pattern

A Pattern is a saved report of recurring behavior, with supporting traces,
its relevance, and a suggested next action.

Select **Patterns** in the project sidebar to see every Pattern reported for the
project. Open one and read its report. Check:

- **Summary** for the recurring behavior Loop found.
- **Evidence** for the traces and spans that support the finding.
- **Suggested fix** for the smallest useful next action.

Treat a Pattern as a starting point for investigation.

![A Pattern report summarizes the behavior, suggests a fix, and links supporting traces.](assets/02-pattern-report.png)

## Step 3: Inspect the evidence trace

The Pattern report links to its evidence traces. Open one in the side panel and
start with the `chat_turn` root, which is one customer turn. Compare the original request with the
final response, then expand the model and tool spans to see how the agent
produced that outcome.

The trace also includes a Pattern span. Select it to see the Pattern attached to
that trace and the evidence relationship.

![A Pattern evidence span connects the trace to its reported Pattern.](assets/02-pattern-evidence-span.png)

A trace can have several Pattern spans, each describing a different recurring
behavior.

## Step 4: Focus on customer email drafting

Continue the investigation with:

~~~text
Investigate customer email drafts in learn-bt. Find chat_turn traces with both
lookup_customer and draft_email where the drafted recipient differs from the
CRM primary_contact.email. Exclude internal-team or generic-mailbox drafts,
explicitly requested alternate recipients, and ambiguous account lookups.
Link the evidence and show the CRM email and drafted recipient for each case.
Also identify recurring writing issues, such as unresolved placeholders.
Distinguish confirmed evidence from hypotheses. Do not create a dataset yet.
~~~

Inspect the cited tool outputs yourself. Patterns retain findings and evidence
for later review. You can run Pattern discovery or a separate Loop
investigation automatically on a daily, weekly, interval, or custom schedule.
An automation can also send its results to Slack, PagerDuty, or a webhook, so
the team can review new findings where it already works.

## If you need more sample traffic

If fresh traffic you generated contains no email mismatches, replay the included
snapshot, which contains recipient mismatches, then repeat the investigation:

~~~bash
uv run --env-file .env python -m scripts.seed_default --project learn-bt
~~~
