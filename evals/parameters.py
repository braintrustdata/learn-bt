"""Saved eval parameters for the Sales Assistant.

Build a versioned parameters object from the agent's config and push it so its
values are editable and versioned in Braintrust. 

Push with:

    bt functions push evals/parameters.py

The reference implementation is in
exercises/4-human-review/03-remote-eval-server.solution.md.
"""

import sys
from pathlib import Path
import braintrust
from pydantic import BaseModel, Field, create_model

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent.config import DEFAULT_CONFIG

# project = braintrust.projects.create(name="learn-bt") #idempotent operation

# project.parameters.create(TODO: implement the parameters object)