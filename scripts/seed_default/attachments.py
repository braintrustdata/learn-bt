"""Finding and rewriting Braintrust attachment references inside span payloads.

A reference is an inline object nested anywhere in a span::

    {"type": "braintrust_attachment", "key": ..., "filename": ..., "content_type": ...}

The key addresses the bytes in the org's object store, so a reference only
resolves inside the org it was uploaded to.
"""

from __future__ import annotations

from typing import Any, Callable, Iterator

ATTACHMENT_TYPE = "braintrust_attachment"


def _is_reference(value: Any) -> bool:
    return isinstance(value, dict) and value.get("type") == ATTACHMENT_TYPE and "key" in value


def iter_references(value: Any) -> Iterator[dict[str, Any]]:
    if _is_reference(value):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_references(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_references(item)


def rewrite(value: Any, replace: Callable[[dict[str, Any]], dict[str, Any]]) -> Any:
    """Return a copy of ``value`` with each attachment reference passed through ``replace``."""
    if _is_reference(value):
        return replace(value)
    if isinstance(value, dict):
        return {k: rewrite(v, replace) for k, v in value.items()}
    if isinstance(value, list):
        return [rewrite(v, replace) for v in value]
    return value
