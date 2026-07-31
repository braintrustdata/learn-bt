"""Runtime configuration for the Sales Assistant agent.

Everything that changes how the agent behaves at runtime lives here: the model,
the sampling parameters, the prompt messages, and the tool descriptions. Keeping
these in one typed object makes two later exercises natural:

  * Tuning: change a value here and re-run to see the effect on quality.
  * Remote evals: the same fields are exposed as eval parameters, so an SME can
    tune the agent from the Braintrust UI without touching code.

The ``system_prompt_messages`` field follows the OpenAI chat completions schema,
which is also the schema Braintrust uses for prompts.
"""

import os
from typing import Any

from pydantic import BaseModel, Field

# The base URL the OpenAI client uses for all model routing, read from the
# BASE_URL env var and defaulting to the Braintrust AI gateway.
#
# The gateway is OpenAI-compatible, so you don't need to obtain and manage API
# keys for each model provider. Configure the LLM providers in the Braintrust org
# settings and they will be available through the gateway via the BRAINTRUST_API_KEY.
# If you don't have permissions to manage providers, you may need to reach out to an admin at your org.
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
    tool_descriptions: dict[str, str] = Field(
        default_factory=lambda: {
            "lookup_customer": (
                "Look up a customer account in the CRM by account id (e.g. ACC-1001) "
                "or by company name. Returns account details including the primary "
                "contact, tier, renewal date, and ARR."
            ),
            "get_opportunity": (
                "Get the details of a sales opportunity by its id (e.g. OPP-5001), "
                "including stage, amount, close date, and the next step."
            ),
            "search_knowledge_base": (
                "Search the internal knowledge base for pricing, security, "
                "onboarding, and competitive positioning information. Use this "
                "before making factual claims about the product."
            ),
            "draft_email": (
                "Draft an email to a customer contact. Provide the recipient, a "
                "subject, and the body. Returns the drafted email for review; it is "
                "not sent automatically."
            ),
            "update_crm_record": (
                "Update a field on a CRM account or opportunity record. Provide the "
                "record id, the field name, and the new value."
            ),
        }
    )

    @property
    def system_prompt(self) -> str:
        """Concatenated system message(s) from the OpenAI-style message list."""
        return "\n\n".join(
            m["content"]
            for m in self.system_prompt_messages
            if m.get("role") == "system"
        )


# The default configuration used by the REPL and the seed script.
DEFAULT_CONFIG = AgentConfig()
