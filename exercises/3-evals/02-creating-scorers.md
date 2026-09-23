# 3.2 Create scorers

Add two scorers for the email-drafting dataset. One is a deterministic requirement. The other is a model judgment about whether the email did what the request asked.

The agent's final response is not the email object. Both scorers inspect the run trace, find the **draft_email** tool span, and grade that span's email output.

Open **evals/scorers.py**.

## Step 1: Write the deterministic recipient check

Replace the **valid_email** TODO with:

~~~python
async def valid_email(trace=None):
    placeholder_domains = {"example.com", "example.org", "example.net"}

    if not trace:
        return None

    tool_spans = await trace.get_spans(span_type=["tool"])
    draft = next(
        (s for s in tool_spans if (s.span_attributes or {}).get("name") == "draft_email"),
        None,
    )
    if not draft:
        return None

    recipient = draft.output["email"].get("recipient", "")
    if "@" not in recipient:
        return 0

    return 0 if recipient.split("@")[-1].lower() in placeholder_domains else 1
~~~

This check is cheap and deterministic. It catches a hard requirement that does not need an LLM judge.

## Step 2: Write the email-goal judge

Replace the prompt TODO with:

~~~python
scorer_prompt = """
An account executive made this request:
{{input.prompt}}

The assistant drafted this email:
Subject: {{output.subject}}
Body: {{output.body}}

Does the drafted email address the requested action? A request can have several
parts. Grade only whether the email addresses the email-related part.

Y: yes
N: no
"""
~~~

Then replace the **email_goal_reached** TODO with:

~~~python
async def email_goal_reached(input=None, trace=None):
    if not trace:
        return None

    tool_spans = await trace.get_spans(span_type=["tool"])
    draft = next(
        (s for s in tool_spans if (s.span_attributes or {}).get("name") == "draft_email"),
        None,
    )
    if not draft:
        return None

    return email_goal_reached_scorer(input=input, output=draft.output["email"])
~~~

A judge can assess whether the email addresses the account executive's intent, which is not a reliable format check.

## Step 3: Register the scorers

Replace the two registration TODOs with:

~~~python
project.scorers.create(
    name="Valid email",
    slug="valid-email",
    parameters=TraceParams,
    handler=valid_email,
)

project.scorers.create(
    name="Email Goal Reached",
    slug="email-goal-reached",
    parameters=JudgeParams,
    handler=email_goal_reached,
)
~~~

The Pydantic parameter models declare what data each scorer receives.

## Step 4: Push and inspect

Push from inside **evals**:

~~~bash
cd evals
bt functions push scorers.py --env-file ../.env
~~~

Open **learn-bt** in Braintrust. Confirm that **Valid email** and **Email Goal Reached** appear as project scorers. On later edits, run the same command with **--if-exists replace**.

## Solution

See [02-creating-scorers.solution.md](02-creating-scorers.solution.md).
