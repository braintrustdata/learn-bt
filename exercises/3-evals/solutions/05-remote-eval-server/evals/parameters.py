"""Saved eval parameters for the Sales Assistant."""

import sys
from pathlib import Path

import braintrust
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.config import DEFAULT_CONFIG

project = braintrust.projects.create(name="learn-bt")


class MaxTurnsParam(BaseModel):
    value: int = Field(
        default=DEFAULT_CONFIG.max_turns,
        description="The most model calls a single agent run may make.",
    )


project.parameters.create(
    name="Sales Assistant Parameters",
    slug="sales-assistant-parameters",
    description="Tunable configuration for the Sales Assistant agent.",
    schema={
        "main": {
            "type": "prompt",
            "description": "Agent's main prompt",
            "default": {
                "prompt": {
                    "type": "chat",
                    "messages": DEFAULT_CONFIG.system_prompt_messages,
                },
                "options": {"model": DEFAULT_CONFIG.model},
            },
        },
        "max_turns": MaxTurnsParam,
    },
)
