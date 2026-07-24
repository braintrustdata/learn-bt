# Solution: Create scorers

Full implementation for `evals/scorers.py`:

```python
import braintrust
from autoevals import LLMClassifier
from pydantic import BaseModel

project = braintrust.projects.create(name="sales-assistant")


# --- Code-based scorer -----------------------------------------------------
class LengthParams(BaseModel):
    output: str


def within_length_budget(output: str):
    """Reward concise answers. Full credit under 800 characters."""
    length = len(output or "")
    if length == 0:
        return {"score": 0.0, "metadata": {"length": 0, "reason": "empty output"}}
    score = 1.0 if length <= 800 else max(0.0, 1.0 - (length - 800) / 800)
    return {"score": score, "metadata": {"length": length}}


# --- LLM-judge scorer ------------------------------------------------------
_quality_classifier = LLMClassifier(
    name="response_quality",
    prompt_template="""You are grading a Sales Assistant's reply to an account executive.

Request:
{{input}}

Reply:
{{output}}

Grade the reply on whether it is helpful and grounded. A good reply addresses the
request and does not invent account details, pricing, or security commitments.

G: helpful and grounded
P: partially helpful, or mixes in unsupported claims
B: unhelpful, or clearly invents facts

Answer:""",
    choice_scores={"G": 1.0, "P": 0.5, "B": 0.0},
    use_cot=True,
)


class ResponseQualityParams(BaseModel):
    input: str
    output: str


def response_quality(input: str, output: str):
    return _quality_classifier(input=input, output=output)


# --- Register for push -----------------------------------------------------
project.scorers.create(
    name="Within length budget",
    slug="within-length-budget",
    description="Deterministic: reward concise answers.",
    parameters=LengthParams,
    handler=within_length_budget,
    metadata={"__pass_threshold": 0.5},
)

project.scorers.create(
    name="Response quality",
    slug="response-quality",
    description="LLM judge: is the reply helpful and grounded?",
    parameters=ResponseQualityParams,
    handler=response_quality,
    metadata={"__pass_threshold": 0.5},
)
```

Push:

```bash
cd evals
bt functions push scorers.py
```

## Notes

- The code scorer is cheap and deterministic, good for hard rules. The LLM judge
  captures fuzzy quality; `use_cot=True` makes it reason before choosing, which
  improves reliability. Its model call routes through the gateway.
- `project.scorers.create(...)` registers each scorer for the push. The Pydantic
  `parameters` model declares what the scorer receives.
- Braintrust bundles `autoevals`, `braintrust`, `openai`, `pydantic`, and
  `requests` by default. For other packages, pass `--requirements`.
- `__pass_threshold` sets the score at or above which a row counts as passing.
