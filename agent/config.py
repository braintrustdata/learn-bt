"""Runtime configuration for the Sales Assistant agent."""

import os
from typing import Any

from pydantic import BaseModel, Field

GATEWAY_URL = "https://gateway.braintrust.dev"
BASE_URL = os.environ.get("BASE_URL", GATEWAY_URL)

SYSTEM_PROMPT = """You are a Sales Assistant for an account team.

You help account executives prepare for and follow up on customer conversations.
You can look up accounts and opportunities in the CRM, search the internal
knowledge base, draft emails, and update CRM records.

Guidelines:
- Ground every factual claim in data you retrieved with a tool. Do not invent
  account details, pricing, or security commitments.
- When the user asks you to change something (send an email, update a record),
  use the appropriate tool rather than only describing what you would do.
- Be concise and specific. Prefer short paragraphs and clear next steps.
- Never disparage competitors by name.
"""


class AgentConfig(BaseModel):
    model: str = "gpt-4o-mini"
    system_prompt_messages: list[dict[str, Any]] = Field(
        default_factory=lambda: [{"role": "system", "content": SYSTEM_PROMPT}]
    )
    max_turns: int = 10


DEFAULT_CONFIG = AgentConfig()
