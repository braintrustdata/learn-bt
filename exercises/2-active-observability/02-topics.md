# 2.2 Understand usage with Topics

You can find individual requests with search and SQL. Now the account team wants
to know how people use the assistant, whether for account research, customer
follow-ups, CRM updates, or something else. Topics classifies traffic so you can inspect that
usage distribution without reading every conversation.

## Step 1: Enable Topics and group conversations

Open **learn-bt**, then **Topics**, and enable classification. Configure the
Topics automation's **Scope** to **Group**, with **Group by** set to
`metadata.session_id` and **Apply to** set to **First trace in group** for these
completed conversations. Save the settings. Choose to backfill existing logs so
the seeded or replayed traffic is included.

Each `chat_turn` remains its own trace. The shared session ID lets Topics analyze
the full conversation, so a follow-up such as "draft the email" is interpreted
with the account context from earlier turns. See the
[Topics grouping instructions](https://www.braintrust.dev/docs/observe/topics/manage#group-traces-into-conversations)
for the grouping controls.

Topics runs in the background and uses your organization's Topics credits. Processing all the traces may take some time.

![Topics groups Sales Assistant traffic and links to source traces.](assets/05-topics-scatterplot-trace.png)

## Step 2: Inspect the usage distribution

Open the **Task** facet. Identify the largest task groups, then open several
conversations in a group related to customer follow-ups or email drafting.
Check whether their labels fit the actual requests and tool calls.
