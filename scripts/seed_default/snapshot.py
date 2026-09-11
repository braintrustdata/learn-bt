"""Reading the recorded log snapshot off disk.

    logs.jsonl          one span per line, in the Braintrust span format
    attachments/<key>   the raw bytes of each attachment

Attachment references in the spans are keyed by content hash, which is also the
name of the file holding those bytes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SNAPSHOT_DIR = Path(__file__).parent / "snapshot"

LOGS_FILE = "logs.jsonl"
ATTACHMENTS_DIR = "attachments"

# Span fields the ingest API accepts. Everything else a query returns is either
# server-owned (``_xact_id``, ``audit_data``, ``org_id``) or scoped to the
# project the snapshot was recorded from (``origin``, ``facets``).
SPAN_FIELDS = (
    "id",
    "span_id",
    "root_span_id",
    "span_parents",
    "span_attributes",
    "input",
    "output",
    "expected",
    "error",
    "scores",
    "metadata",
    "tags",
    "metrics",
    "context",
)

# Attributes the source project's own identity, not the span's shape.
DROPPED_SPAN_ATTRIBUTES = ("created_by_api_key_id", "created_by_user_id", "exec_counter")


@dataclass
class Snapshot:
    spans: list[dict[str, Any]]
    attachments_dir: Path

    def attachment_path(self, key: str) -> Path:
        """The file holding the bytes for ``key``, whatever extension it was saved with."""
        matches = sorted(self.attachments_dir.glob(f"{key}.*"))
        if not matches:
            raise FileNotFoundError(f"No attachment file for key {key} in {self.attachments_dir}")
        return matches[0]


def load(directory: Path = SNAPSHOT_DIR) -> Snapshot:
    logs_path = directory / LOGS_FILE
    if not logs_path.exists():
        raise FileNotFoundError(
            f"No recorded logs at {logs_path}. Rebuild the snapshot with "
            "`uv run python -m scripts.seed_default.fetch`."
        )

    spans = [json.loads(line) for line in logs_path.read_text().splitlines() if line.strip()]
    return Snapshot(spans=spans, attachments_dir=directory / ATTACHMENTS_DIR)
