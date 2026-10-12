# 2.3 Discover recurring failures with Loop and Patterns

Active observability applies AI to the traces you already collect. Start with a
question in Loop, turn a supported recurring behavior into a Pattern, then
inspect the Pattern's evidence in the trace itself.

Use instrumented Sales Assistant traffic to investigate whether the agent
completes AE requests correctly. If Topics classifications are available, use
the task distribution to inform the investigation.

## Step 1: Discover candidate failures

Open **learn-bt**, then select **Loop** in the project sidebar. Start a new
thread and ask:

~~~text
Review the current Sales Assistant logs. Identify up to three recurring behaviors or possible failure modes. For each one, link the supporting traces, explain the evidence, and say whether it is worth tracking.
~~~

Loop investigates the project and returns an evidence-backed response.

![Loop groups findings from Sales Assistant logs into reported Patterns.](assets/02-loop-investigation-and-reported-patterns.png)

## Step 2: Read a Pattern

When Loop identifies a recurring behavior, it reports a Pattern. A Pattern is a
saved report, not a single trace. It summarizes the behavior, explains why it
matters, links to the supporting evidence, and suggests a next action.

Select **Patterns** in the project sidebar to see every Pattern reported for the
project. Open one and read its report. Check:

- **Summary** for the recurring behavior Loop found.
- **Evidence** for the traces and spans that support the finding.
- **Suggested fix** for the smallest useful next action.

Treat a Pattern as a starting point for investigation. Before you act on it,
confirm that the cited evidence represents the same behavior across several
traces.

![A Pattern report summarizes the behavior, suggests a fix, and links supporting traces.](assets/02-pattern-report.png)

## Step 3: Inspect the evidence trace

The Pattern report links to its evidence traces. Open one in the side panel and
start with the `chat_turn` root, which is one customer turn. Compare the original request with the
final response, then expand the model and tool spans to see how the agent
produced that outcome.

The trace also includes a Pattern span. Select it to see the Pattern attached to
that trace and the evidence relationship. This span records an observability
finding. It does not represent work that the Sales Assistant performed during
the request.

![A Pattern evidence span connects the trace to its reported Pattern.](assets/02-pattern-evidence-span.png)

One trace can support more than one Pattern. In that case, the same trace has
multiple Pattern spans. Read each one separately because they can describe
different recurring behaviors in the same agent run.

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

Inspect the cited tool outputs yourself. Save links to confirmed mismatches and
at least one draft that needs writing edits. If fresh traffic contains no
mismatches, replay the included snapshot with
`uv run --env-file .env python -m scripts.seed_default --project learn-bt`,
then repeat the investigation. Do not label a correct draft as a failure to
complete the exercise.

For a team operating this assistant, revisiting the investigation daily would
help identify new failures. Patterns retain findings and evidence for review;
this exercise uses a one-time investigation and does not configure a schedule.

Record the confirmed failures, their source links, and the evidence supporting
each finding.
