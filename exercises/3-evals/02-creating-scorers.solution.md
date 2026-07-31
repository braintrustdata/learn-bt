# Solution: Create scorers

```python
import os

import braintrust
from autoevals import LLMClassifier
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

project = braintrust.projects.create(name="learn-bt")  # Idempotent operation

# This example uses the Braintrust Gateway for LLM calls. This judge client is
# provided as reference to use as the client for the LLM Judge
judge_client = OpenAI(
    base_url=os.getenv("BRAINTRUST_AI_GATEWAY_URL") or "https://gateway.braintrust.dev",
    api_key=os.environ["BRAINTRUST_API_KEY"],
    default_headers={"x-bt-org-name": os.getenv("BRAINTRUST_ORG_NAME", "")},
)


# --- Code scorer -----------------------------------------------------------
class TraceParams(BaseModel):
    trace: dict


async def valid_email(trace=None):
    """Assert the drafted email is addressed to a real, non-placeholder recipient."""
    
    PLACEHOLDER_DOMAINS = {"example.com", "example.org", "example.net"}
    
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
    domain = recipient.split("@")[-1].lower()
    return 0 if domain in PLACEHOLDER_DOMAINS else 1


# --- LLM-judge scorer ------------------------------------------------------
scorer_prompt = """
An account executive made this request:
{{input.prompt}}

The assistant drafted this email in response:
Subject: {{output.subject}}
Body: {{output.body}}

Does the drafted email address the request?
The email must specifically fully address the requested action, and not just repeat the request.

Y: yes
N: no
"""

email_goal_reached_scorer = LLMClassifier(
    name="Email Goal Reached",
    prompt_template=scorer_prompt,
    choice_scores={"Y": 1, "N": 0},
    use_cot=True,
    client=judge_client,
)


class JudgeParams(BaseModel):
    input: dict
    trace: dict


async def email_goal_reached(input=None, trace=None):
    """Grade whether the drafted email addresses the request."""
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

# --- Register for push -----------------------------------------------------
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

```

Push to Braintrust:

```bash
cd evals
bt functions push scorers.py
```

Verify these scorers show up in the Braintrust project.

## Notes

- **Both scorers filter the trace to the drafted email.** The agent's output is
  its final reply, not the email object, so each scorer takes the run's `trace`,
  fetches the `tool` spans with `await trace.get_spans(span_type=["tool"])`, picks the one named `draft_email`, and grades `draft.output["email"]` 
- `parameters` is a Pydantic model declaring what the scorer receives, required for `project.scorers.create(...)` to push.
- For successive push commands, use `--if-exists replace` flag to push a new version.
