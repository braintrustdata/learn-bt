# 3.3 Review email failures with an account-team expert [UI]

The previous section used deterministic and LLM-as-a-judge scorers. This
exercise adds human review in Braintrust, where an account-team expert reviews
an AI output and explains the decision. Human review is useful for nuanced
business criteria, specialized domain knowledge, and gold-standard labels that
you can use to validate automated scoring.

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

This shows the review form only on `draft_email` spans, which keeps reviewers
focused on the exact output they are evaluating rather than unrelated model and
tool spans.

## Step 3: Review the investigation examples

Save the scorer. Open a trace with a CRM recipient mismatch, assign
its `draft_email` span to yourself in **Review**, and inspect the trace with
**Customer email review**. Submit a written review that explains why the draft
does not satisfy the AE's request.

Return to each reviewed span and confirm the text appears at `metadata.review`. Use the saved reviews when curating the dataset and checking automated judges.
