# 3.1 Create a human review intake form [UI]

When we have codified our failure taxonomy and review process, we can create structured intake forms for human review so that SMEs can inspect and provide feedback on traces in a standardized way. In this exercise,
you will add a human-review scorer to capture feedback on email quality, which will be written to the trace directly.

## Step 1: Create the scorer

In Braintrust, open **Settings**, then **Human review**. You can also open
**Logs**, then **Review**, then **Manage scores**.

Create a scorer with these values:

~~~text
Name: Email quality review
Response type: Free-form text
Metadata path: review
~~~

A free-form response lets the reviewer explain why an email is ready or what
needs to change. The metadata path stores that explanation at
`metadata.review`.

## Step 2: Limit it to drafted emails

In the scorer visibility settings, add:

~~~sql
span_attributes.name = "draft_email"
~~~

The review applies to the drafted email. This filter hides the scorer on
unrelated model calls and tool spans, keeping the review workflow focused.

## Step 3: Submit one review

Save the scorer. Open a trace with a `draft_email` span, assign that span to
yourself in **Review**, and enter a short review. This mirrors the workflow of a
domain expert reviewing items from a shared queue. The domain expert is notified when there are items in their review queue, they open the queue and can inspect the trace via the custom view we've created, and use the human review scorers to provide structured grading. This annotation can then be used in downstream, offline evals.

Return to the span and confirm that the text appears at:

~~~text
metadata.review
~~~

The expert judgment now sits alongside automatic scores and can inform future
scorer calibration.
