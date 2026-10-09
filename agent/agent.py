"""The Sales Assistant agent.
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Sequence

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageFunctionToolCall

from . import tools
from .config import DEFAULT_CONFIG, AgentConfig

load_dotenv()


class AgentError(RuntimeError):
    """Raised when a run cannot produce a final answer."""


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    if os.environ.get("DISABLE_BRAINTRUST_GATEWAY"):
        return OpenAI(
            base_url=os.environ["BASE_URL"]
        )

    return OpenAI(
        base_url=os.environ["BASE_URL"],
        api_key=os.environ["BRAINTRUST_API_KEY"],
        default_headers={"x-bt-org-name": os.environ.get("BRAINTRUST_ORG_NAME", "")},
    )


@dataclass
class InputFile:
    """A file sent to the model as multimodal input."""

    data: bytes
    media_type: str
    filename: str = "attachment"

    @classmethod
    def from_path(cls, path: str | Path) -> InputFile:
        """Read a file from the local filesystem."""
        p = Path(path)
        media_type = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        return cls(data=p.read_bytes(), media_type=media_type, filename=p.name)

    @classmethod
    def from_dataset_attachment(cls, attachment: Any) -> InputFile:
        """Read a Braintrust attachment hydrated from a dataset row."""
        return cls(
            data=attachment.data,
            media_type=attachment.reference["content_type"],
            filename=attachment.reference.get("filename", "attachment"),
        )

    def as_content_part(self) -> dict[str, Any]:
        """Render the file as a content part in a chat message."""
        url = f"data:{self.media_type};base64,{base64.b64encode(self.data).decode()}"
        if self.media_type.startswith("image/"):
            return {"type": "image_url", "image_url": {"url": url}}
        return {"type": "file", "file": {"filename": self.filename, "file_data": url}}


@dataclass
class AgentResult:
    """The output of one chat turn."""

    output: str
    new_messages: list[dict[str, Any]] = field(default_factory=list)


def _user_message(prompt: str, attachments: list[InputFile]) -> dict[str, Any]:
    """Build the user message, as plain text or as text plus attachment parts."""
    if not attachments:
        return {"role": "user", "content": prompt}
    return {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            *(attachment.as_content_part() for attachment in attachments),
        ],
    }


def _tool_message(call: ChatCompletionMessageFunctionToolCall) -> dict[str, Any]:
    result = tools.dispatch(call.function.name, call.function.arguments)
    return {
        "role": "tool",
        "tool_call_id": call.id,
        "content": json.dumps(result),
    }


class Agent:
    def __init__(self, config: AgentConfig = DEFAULT_CONFIG):
        self.config = config

    def chat_turn(
        self,
        prompt: str,
        session_id: str,
        attachments: Sequence[str | Path | InputFile] | None = None,
        history: Sequence[dict[str, Any]] | None = None,
    ) -> AgentResult:
        client = get_client()
        input_files = [
            a if isinstance(a, InputFile) else InputFile.from_path(a)
            for a in attachments or []
        ]
        new_messages = [_user_message(prompt, input_files)]
        tool_specs = tools.tool_specs()
        tool_calls_made = 0

        while True:
            response = client.chat.completions.create(
                model=self.config.model,
                messages=[  # type: ignore
                    *self.config.system_prompt_messages,
                    *(history or []),
                    *new_messages,
                ],
                tools=tool_specs,
            )
            choice = response.choices[0]
            message = choice.message

            new_messages.append(message.model_dump(exclude_none=True))

            if choice.finish_reason == "length":
                raise AgentError("The model's response was cut off by the token limit.")
            if not message.tool_calls:
                return AgentResult(output=message.content or "", new_messages=new_messages)

            for call in message.tool_calls:
                tool_calls_made += 1
                if tool_calls_made > self.config.max_tool_calls:
                    raise AgentError(
                        f"The agent used more than {self.config.max_tool_calls} tool calls."
                    )
                new_messages.append(_tool_message(call))  # type: ignore
