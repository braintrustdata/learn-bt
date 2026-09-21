# 4.2 Create a human review scorer [UI]

Automated scorers give you repeatable checks. A human-review scorer captures the judgment a domain expert makes when the rubric is too nuanced for code or an LLM judge.

## Step 1: Create the scorer

In Braintrust, open **Settings**, then **Human review**. You can also open **Logs**, then **Review**, then **Manage scores**.

Create a scorer with these values:

~~~text
Name: Email quality review
Response type: Free-form text
Metadata path: review
~~~

A free-form response lets the reviewer explain why an email was strong or weak. The metadata path stores that explanation as **metadata.review**.

## Step 2: Limit it to drafted emails

In the scorer visibility settings, add:

~~~sql
span_attributes.name = "draft_email"
~~~

The review is about the drafted email. The filter prevents a reviewer from attaching email feedback to an unrelated model call or tool span.

## Step 3: Submit one review

Save the scorer. Open a trace with a **draft_email** span, assign that span to yourself in **Review**, and enter a short review.

Return to the span and confirm that the text appears at:

~~~text
metadata.review
~~~

That feedback can now sit alongside automatic scores and help calibrate later scorers.
