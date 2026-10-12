"""Saved eval parameters for the Sales Assistant.

Push with: bt functions push evals/parameters.py --env-file .env
"""

import sys
from pathlib import Path
import braintrust
from pydantic import BaseModel, Field, create_model

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent.config import DEFAULT_CONFIG

# project = braintrust.projects.create(name="learn-bt")

# project.parameters.create(TODO: implement the parameters object)
