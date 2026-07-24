# 4.2 Create scorers

Write two scorers in `evals/scorers.py` and push them to Braintrust.

## Task

1. A **code-based scorer**. A deterministic rule with no model call. For example,
   reward concise answers (full credit under some character budget).
2. An **LLM-judge scorer** built with the autoevals `LLMClassifier` class. Have it
   grade whether the agent's reply is helpful and grounded, meaning it does not
   invent account details, pricing, or security commitments.

Register both on the `sales-assistant` project with `project.scorers.create(...)`,
then push:

```bash
cd evals
bt functions push scorers.py
```

Push from inside the `evals/` directory. Relative paths are not supported for
Python scorers.

## Solution

The reference is [`evals/scorers.py`](../../evals/scorers.py) as completed in
[02-creating-scorers.solution.md](02-creating-scorers.solution.md).
