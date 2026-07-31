"""The Sales Assistant agent.

This module wires the config, tools, and Pydantic AI together into a runnable
agent. It is intentionally free of any Braintrust tracing: adding observability
to this agent is the first hands-on exercise. By the end of the workshop this is
the file (and its callers) you will have instrumented and evaluated.
"""

from __future__ import annotations

import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path

from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.tools import Tool
from openai import AsyncOpenAI
from dotenv import load_dotenv

from . import tools
from .config import BASE_URL, DEFAULT_CONFIG, AgentConfig

load_dotenv()


def build_agent(config: AgentConfig = DEFAULT_CONFIG) -> Agent:
    """Construct a Pydantic AI agent from a config object."""
    openai_client = AsyncOpenAI(
        base_url=BASE_URL,
        api_key=os.environ["BRAINTRUST_API_KEY"],
        default_headers={"x-bt-org-name": os.environ.get("BRAINTRUST_ORG_NAME", "")},
    )
    model = OpenAIChatModel(
        config.model,
        provider=OpenAIProvider(openai_client=openai_client),
    )
    tool_objects = [
        Tool(fn, name=name, description=config.tool_descriptions.get(name))
        for name, fn in tools.TOOLS.items()
    ]

    return Agent(
        model=model,
        system_prompt=config.system_prompt,
        tools=tool_objects,
    )


def _load_local_attachment(path: str | Path) -> BinaryContent:
    """Read a file from the local filesystem into a Pydantic AI BinaryContent part."""
    p = Path(path)
    media_type = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return BinaryContent(data=p.read_bytes(), media_type=media_type)


@dataclass
class AgentResult:
    """The output of a single agent run."""

    output: str


def run_agent(
    prompt: str,
    attachments: list[str | Path | BinaryContent] | None = None,
    config: AgentConfig = DEFAULT_CONFIG,
) -> AgentResult:
    """Run the agent once and return its output.

    ``prompt`` is the user's request. ``attachments`` is an optional list passed to
    the model as multimodal input. Each item is either a local file path, which is
    read from disk, or an already-loaded ``BinaryContent`` part.
    """
    agent = build_agent(config)

    user_input: list = [prompt]
    for attachment in attachments or []:
        if isinstance(attachment, BinaryContent):
            user_input.append(attachment)
        else:
            user_input.append(_load_local_attachment(attachment))

    result = agent.run_sync(user_input)
    return AgentResult(output=result.output)
