# 3.1 Review email failures with an account-team expert [UI]

Start with instrumented traces containing candidate email failures. Take the role of
an account-team expert: confirm which drafts are usable and explain what needs
to change. Use the saved **Customer email review** view and a written review
form so feedback stays with the draft's trace.

For this workshop, a customer follow-up should use the intended account's CRM
primary contact unless the AE explicitly requested another recipient. Its subject
and body should be complete, concise, and professional but conversational, with
no unresolved placeholders. These are the criteria you will encode in scorers.

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

## Step 3: Review the investigation examples

Save the scorer. Open a trace with a CRM recipient mismatch, assign
its `draft_email` span to yourself in **Review**, and inspect the trace with
**Customer email review**. Submit a written review that names the CRM recipient,
the actual recipient, and why this is a failure for the AE's request.

Review one draft with a writing issue as well. Name the specific problem, such
as `[Your Name]`, excessive repetition, or an unsuitable tone. If a draft is
acceptable, explain why. Keep links to these examples for testing the scorer.

Return to each reviewed span and confirm the text appears at `metadata.review`.
The custom view's thumbs feedback captures a quick reaction; this form records
the explanation. Human feedback remains on the source spans, providing evidence
for dataset curation and a reference for checking automated judges.
