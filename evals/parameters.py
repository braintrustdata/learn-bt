"""Saved eval parameters for the Sales Assistant (exercise 5.3, part 1).

Build a versioned parameters object from the agent's config and push it so its
values are editable in the UI. Include the model, the temperature, and the system
prompt (use a `prompt`-type parameter for the system prompt). Push with:

    cd evals
    bt functions push parameters.py

The reference implementation is in
exercises/4-human-review/03-remote-eval-server.solution.md.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import braintrust  # noqa: E402

project = braintrust.projects.create(name="sales-assistant")

# TODO: define the parameter schema (model, temperature, system_prompt) and
# register it with project.parameters.create(...).
