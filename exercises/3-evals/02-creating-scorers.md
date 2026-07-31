# 4.2 Create scorers

You have a dataset of real email-drafting requests. To evaluate the agent on
them you need scorers: functions that grade each drafted email. A good eval pairs
two kinds, a cheap deterministic rule and a model-graded judgment, so you catch
both hard failures and fuzzy quality.

Write two scorers in [`evals/scorers.py`](../../evals/scorers.py). Both grade the
drafted email the agent produced (its `recipient`, `subject`, and `body`). The
agent's output is its final reply, not the email object, so each scorer takes the
run's `trace`, fetches the `tool` spans, and pulls the `draft_email` span's output
to grade.

## Task

1. **A code-based scorer, `valid_email`.** A deterministic scorer that validates that the recipient of the drafted email has a "valid" email address. Note: this scorer does not have to be super precise for this exercise. You can keep the business logic simple. The reference solution provided treats the email as valid if it contains an `@` and does not have a placeholder domain such as `@example.com`.

2. **An LLM-judge scorer, `email_goal_reached`.** This should be an LLM Judge scorer that asserts overall if the email drafted resolves the user's request. There are multiple ways in which this can be implemented. The reference solution uses the LLMClassifier class from the Braintrust `autoevals` library.

Register both on the `learn-bt` project with `project.scorers.create(...)`, then
push:

```bash
cd evals
bt functions push scorers.py
```

Push from inside the `evals/` directory. Relative paths are not supported for
Python scorers.

## Solution

The reference is [`evals/scorers.py`](../../evals/scorers.py) as completed in
[02-creating-scorers.solution.md](02-creating-scorers.solution.md).
