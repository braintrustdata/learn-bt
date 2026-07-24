"""Scorers for the Sales Assistant (exercise 4.2).

Implement two scorers here and register them with `project.scorers.create(...)`,
then push with `bt functions push scorers.py` (run from inside this directory).

  1. A deterministic code scorer.
  2. An LLM-judge scorer built with autoevals `LLMClassifier`.

See the exercise for details. The reference implementation is in
exercises/3-evals/02-creating-scorers.solution.md.
"""

import braintrust

project = braintrust.projects.create(name="sales-assistant")

# TODO: implement and register your two scorers.
