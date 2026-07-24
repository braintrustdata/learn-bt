"""Eval for the Sales Assistant (exercise 4.3).

Write an eval that runs the agent over the dataset you curated in 4.1 and scores
it with the scorers you pushed in 4.2. Run with:

    bt eval evals/eval_agent.py

The reference implementation is in
exercises/3-evals/03-executing-an-eval.solution.md.
"""

import sys
from pathlib import Path

# Make the repo root importable so `agent` resolves when run from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# TODO: build the eval (load the dataset, use run_agent as the task, add scorers).
