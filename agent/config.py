"""Runtime configuration for the Sales Assistant agent.

Everything that changes how the agent behaves at runtime lives here: the model,
the sampling parameters, the prompt messages, and the tool descriptions. Keeping
these in one typed object makes two later exercises natural:

  * Tuning: change a value here and re-run to see the effect on quality.
  * Remote evals: the same fields are exposed as eval parameters, so an SME can
    tune the agent from the Braintrust UI without touching code.

The ``messages`` and ``params`` fields follow the OpenAI chat completions schema,
which is also the schema Braintrust uses for prompts.
"""

from pydantic import BaseModel, Field

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


class ModelParams(BaseModel):
    """OpenAI-style sampling parameters."""

    temperature: float = 0.2
    max_tokens: int = 1024
    top_p: float = 1.0


class Message(BaseModel):
    """A single chat message in OpenAI chat completions format."""

    role: str
    content: str


class AgentConfig(BaseModel):
    """The full, tunable configuration for one run of the agent."""

    # All model calls route through the Braintrust AI gateway, which is
    # OpenAI-compatible. This means a single BRAINTRUST_API_KEY reaches every
    # provider and you can change `model` to any supported model (gpt-4o-mini,
    # claude-3-5-sonnet-latest, gemini-2.5-flash, ...) without new keys.
    base_url: str = "https://gateway.braintrust.dev"
    model: str = "gpt-4o-mini"
    params: ModelParams = Field(default_factory=ModelParams)
    messages: list[Message] = Field(
        default_factory=lambda: [Message(role="system", content=SYSTEM_PROMPT)]
    )
    # Tool descriptions are configuration because the wording materially affects
    # when and how the model chooses to call each tool.
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
        return "\n\n".join(m.content for m in self.messages if m.role == "system")


# The default configuration used by the REPL and the seed script.
DEFAULT_CONFIG = AgentConfig()
