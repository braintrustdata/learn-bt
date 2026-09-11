"""Seed a Braintrust project by replaying pre-recorded logs, with no model calls.

Usage:
    uv run python -m scripts.seed_default --project my-project

Requires BRAINTRUST_API_KEY (a .env file is loaded if present).
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any

import braintrust
import requests
from dotenv import load_dotenv

from . import attachments as attachment_refs
from . import snapshot as snapshot_module

load_dotenv()

INSERT_BATCH_SIZE = 100
UPLOAD_WORKERS = 8


def _api_url() -> str:
    return os.environ.get("BRAINTRUST_API_URL", "https://api.braintrust.dev").rstrip("/")


def _upload_attachments(
    recorded: snapshot_module.Snapshot, references: list[dict[str, Any]]
) -> dict[str, str]:
    """Upload each referenced file once, mapping its snapshot key to the new key."""

    def upload(reference: dict[str, Any]) -> tuple[str, str]:
        attachment = braintrust.Attachment(
            data=str(recorded.attachment_path(reference["key"])),
            filename=reference["filename"],
            content_type=reference["content_type"],
        )
        status = attachment.upload()
        if status.get("upload_status") != "done":
            raise RuntimeError(
                f"Failed to upload {reference['filename']}: {status.get('error_message')}"
            )
        return reference["key"], attachment.reference["key"]

    by_key = {reference["key"]: reference for reference in references}
    with ThreadPoolExecutor(max_workers=UPLOAD_WORKERS) as executor:
        return dict(executor.map(upload, by_key.values()))


def _span_start(span: dict[str, Any]) -> float:
    return (span.get("metrics") or {}).get("start", 0.0)


def _prepare_span(
    span: dict[str, Any],
    shift: float,
    attachment_keys: dict[str, str],
) -> dict[str, Any]:
    """Rewrite one span's attachment references and timestamps for insertion."""
    def replace_attachment(reference: dict[str, Any]) -> dict[str, Any]:
        return {**reference, "key": attachment_keys[reference["key"]]}

    event = attachment_refs.rewrite(span, replace_attachment)

    metrics = dict(event.get("metrics") or {})
    for field in ("start", "end"):
        if field in metrics:
            metrics[field] += shift
    if metrics:
        event["metrics"] = metrics
    if "start" in metrics:
        event["created"] = datetime.fromtimestamp(metrics["start"], tz=timezone.utc).isoformat()

    return event


def _insert(session: requests.Session, project_id: str, events: list[dict[str, Any]]) -> None:
    response = session.post(
        f"{_api_url()}/v1/project_logs/{project_id}/insert", json={"events": events}
    )
    if not response.ok:
        raise SystemExit(f"Insert failed ({response.status_code}): {response.text}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed a project with pre-recorded Sales Assistant logs."
    )
    parser.add_argument("--project", required=True,
                        help="Braintrust project to seed. Created if it does not exist.")
    args = parser.parse_args()

    if not os.environ.get("BRAINTRUST_API_KEY"):
        raise SystemExit("BRAINTRUST_API_KEY is not set.")

    recorded = snapshot_module.load()
    spans = recorded.spans
    traces = len({span["root_span_id"] for span in spans})
    print(f"Loaded {len(spans)} recorded spans across {traces} traces.")

    project_id = braintrust.init_logger(project=args.project).id
    print(f"Seeding project {args.project!r} ({project_id}).")

    references = [
        reference for span in spans for reference in attachment_refs.iter_references(span)
    ]
    attachment_keys: dict[str, str] = {}
    if references:
        files = len({reference["key"] for reference in references})
        print(f"Uploading {files} attachments for {len(references)} references...")
        attachment_keys = _upload_attachments(recorded, references)

    # One shift for the whole set, landing the last recorded span at the present
    # moment and leaving every span's position relative to the others intact.
    shift = time.time() - max(map(_span_start, spans))
    events = [_prepare_span(span, shift, attachment_keys) for span in spans]

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {os.environ['BRAINTRUST_API_KEY']}"
    for i in range(0, len(events), INSERT_BATCH_SIZE):
        batch = events[i : i + INSERT_BATCH_SIZE]
        _insert(session, project_id, batch)
        print(f"  inserted {min(i + len(batch), len(events))}/{len(events)} spans")

    print(f"Done. {traces} traces are in {args.project}.")


if __name__ == "__main__":
    main()
