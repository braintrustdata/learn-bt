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
from pydantic_ai.settings import ModelSettings
from pydantic_ai.tools import Tool

from . import tools
from .config import DEFAULT_CONFIG, AgentConfig


def build_agent(config: AgentConfig = DEFAULT_CONFIG) -> Agent:
    """Construct a Pydantic AI agent from a config object.

    The model is served through the Braintrust AI gateway (an OpenAI-compatible
    endpoint), so a single BRAINTRUST_API_KEY is all that is needed and the model
    can be swapped by changing the config. Tools are registered with the
    descriptions from the config so that wording is a tunable parameter, not
    something buried in a docstring.
    """
    model = OpenAIChatModel(
        config.model,
        provider=OpenAIProvider(
            base_url=config.base_url,
            api_key=os.environ["BRAINTRUST_API_KEY"],
        ),
    )
    tool_objects = [
        Tool(fn, name=name, description=config.tool_descriptions.get(name))
        for name, fn in tools.TOOLS.items()
    ]
    return Agent(
        model=model,
        system_prompt=config.system_prompt,
        tools=tool_objects,
        model_settings=ModelSettings(
            temperature=config.params.temperature,
            max_tokens=config.params.max_tokens,
            top_p=config.params.top_p,
        ),
    )


def _load_attachment(path: str | Path) -> BinaryContent:
    """Read a file from disk into a Pydantic AI BinaryContent part."""
    p = Path(path)
    media_type = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return BinaryContent(data=p.read_bytes(), media_type=media_type)


@dataclass
class AgentResult:
    """The output of a single agent run, plus any write-tool side effects."""

    output: str
    writes: list[dict]


def run_agent(
    prompt: str,
    attachments: list[str | Path] | None = None,
    config: AgentConfig = DEFAULT_CONFIG,
) -> AgentResult:
    """Run the agent once and return its output.

    ``prompt`` is the user's request. ``attachments`` is an optional list of file
    paths (for example a PDF sent by a customer) that are passed to the model as
    multimodal input.
    """
    tools.WRITE_LOG.clear()
    agent = build_agent(config)

    user_input: list = [prompt]
    for attachment in attachments or []:
        user_input.append(_load_attachment(attachment))

    result = agent.run_sync(user_input)
    return AgentResult(output=result.output, writes=list(tools.WRITE_LOG))
