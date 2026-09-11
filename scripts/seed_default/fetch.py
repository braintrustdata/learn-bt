"""Record a project's logs into the snapshot that scripts.seed_default replays.

Maintainer tool, not part of the workshop.

Usage:
    uv run python -m scripts.seed_default.fetch --source-project my-project
    uv run python -m scripts.seed_default.fetch --source-project my-project --traces 50

Requires BRAINTRUST_API_KEY with read access to the source project.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from . import attachments as attachment_refs
from .snapshot import (
    ATTACHMENTS_DIR,
    DROPPED_SPAN_ATTRIBUTES,
    LOGS_FILE,
    SNAPSHOT_DIR,
    SPAN_FIELDS,
)

load_dotenv()

DEFAULT_TRACES = 100

# BTQL caps a single query at 1000 rows, so traces are fetched a chunk at a time.
BTQL_MAX_LIMIT = 1000
TRACES_PER_QUERY = 25

# Automation output (Patterns, online scorers) points at rules that live in the
# source project, so it would dangle in a replayed copy.
SKIPPED_SPAN_TYPES = {"automation"}

# App-managed metadata (review list assignments and the like) is prefixed with
# a tilde and refers to users and lists in the source org.
INTERNAL_METADATA_PREFIX = "~__bt"


def _api_url() -> str:
    return os.environ.get("BRAINTRUST_API_URL", "https://api.braintrust.dev").rstrip("/")


def _session() -> requests.Session:
    api_key = os.environ.get("BRAINTRUST_API_KEY")
    if not api_key:
        raise SystemExit("BRAINTRUST_API_KEY is not set.")
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {api_key}"
    return session


def _resolve_project(session: requests.Session, name: str) -> tuple[str, str]:
    """Return the (project_id, org_id) of the named project."""
    response = session.get(f"{_api_url()}/v1/project", params={"project_name": name})
    response.raise_for_status()
    projects = response.json().get("objects") or []
    if not projects:
        raise SystemExit(f"No project named {name!r} is visible with this API key.")
    return projects[0]["id"], projects[0]["org_id"]


def _btql(session: requests.Session, query: str) -> list[dict[str, Any]]:
    response = session.post(f"{_api_url()}/btql", json={"query": query, "fmt": "json"})
    if not response.ok:
        raise SystemExit(f"BTQL query failed ({response.status_code}): {response.text}\n{query}")
    return response.json()["data"]


def _fetch_spans(session: requests.Session, project_id: str, traces: int) -> list[dict[str, Any]]:
    """Fetch every span belonging to the ``traces`` most recent traces."""
    roots = _btql(
        session,
        f"select: root_span_id from: project_logs('{project_id}') "
        f"filter: is_root sort: created desc limit: {traces}",
    )
    root_span_ids = [row["root_span_id"] for row in roots]

    spans: list[dict[str, Any]] = []
    for start in range(0, len(root_span_ids), TRACES_PER_QUERY):
        chunk = root_span_ids[start : start + TRACES_PER_QUERY]
        id_list = ", ".join(f"'{root_span_id}'" for root_span_id in chunk)
        page = _btql(
            session,
            f"select: * from: project_logs('{project_id}') "
            f"filter: root_span_id IN ({id_list}) limit: {BTQL_MAX_LIMIT}",
        )
        if len(page) == BTQL_MAX_LIMIT:
            raise SystemExit(
                f"A chunk of {len(chunk)} traces filled the {BTQL_MAX_LIMIT}-row query limit, so "
                "some spans would be missing. Lower TRACES_PER_QUERY and re-run."
            )
        spans.extend(page)

    return spans


def _clean(span: dict[str, Any]) -> dict[str, Any] | None:
    """Reduce a queried row to the portable span fields, or drop it entirely."""
    span_attributes = {
        k: v for k, v in (span.get("span_attributes") or {}).items()
        if k not in DROPPED_SPAN_ATTRIBUTES
    }
    if span_attributes.get("type") in SKIPPED_SPAN_TYPES:
        return None

    cleaned = {
        field: span[field]
        for field in SPAN_FIELDS
        if field in span and span[field] is not None
    }
    cleaned["span_attributes"] = span_attributes

    metadata = {
        k: v for k, v in (cleaned.get("metadata") or {}).items()
        if not k.startswith(INTERNAL_METADATA_PREFIX)
    }
    if metadata:
        cleaned["metadata"] = metadata
    else:
        cleaned.pop("metadata", None)

    return cleaned


def _extension(filename: str, content_type: str) -> str:
    suffix = Path(filename).suffix
    return suffix or mimetypes.guess_extension(content_type) or ".bin"


def _download_attachments(
    session: requests.Session, org_id: str, spans: list[dict[str, Any]], directory: Path
) -> dict[str, str]:
    """Save the bytes behind every attachment reference, keyed by content hash.

    One file usually appears under several keys, because the agent passes it
    through several spans and the SDK uploads it separately for each. Keying by
    content hash stores those copies once. The source keys do not survive into
    the snapshot: they address the source org's object store, and the replay
    uploads and re-keys everything anyway.
    """
    references = {
        reference["key"]: reference
        for span in spans
        for reference in attachment_refs.iter_references(span)
    }
    if not references:
        return {}

    directory.mkdir(parents=True, exist_ok=True)
    digests: dict[str, str] = {}
    for i, (key, reference) in enumerate(sorted(references.items()), start=1):
        filename = reference.get("filename") or "attachment"
        content_type = reference.get("content_type") or "application/octet-stream"
        metadata = session.get(
            f"{_api_url()}/attachment",
            params={
                "key": key,
                "filename": filename,
                "content_type": content_type,
                "org_id": org_id,
            },
        )
        metadata.raise_for_status()
        download_url = metadata.json()["downloadUrl"]

        contents = requests.get(download_url)
        contents.raise_for_status()

        digest = hashlib.sha256(contents.content).hexdigest()[:16]
        (directory / f"{digest}{_extension(filename, content_type)}").write_bytes(contents.content)
        digests[key] = digest
        print(f"  [{i}/{len(references)}] {filename} -> {digest} ({len(contents.content):,} bytes)")

    return digests


def main() -> None:
    parser = argparse.ArgumentParser(description="Record project logs into a replayable snapshot.")
    parser.add_argument("--source-project", required=True,
                        help="Project to record traces from.")
    parser.add_argument("--traces", type=int, default=DEFAULT_TRACES,
                        help="Number of most recent traces to record.")
    parser.add_argument("--out", type=Path, default=SNAPSHOT_DIR,
                        help="Directory to write the snapshot into.")
    args = parser.parse_args()

    session = _session()
    project_id, org_id = _resolve_project(session, args.source_project)

    print(f"Fetching the {args.traces} most recent traces from {args.source_project}...")
    spans = [cleaned for span in _fetch_spans(session, project_id, args.traces)
             if (cleaned := _clean(span))]
    traces = sum(1 for span in spans if not span.get("span_parents"))
    print(f"Fetched {len(spans)} spans across {traces} traces.")

    args.out.mkdir(parents=True, exist_ok=True)
    print("Downloading attachments...")
    digests = _download_attachments(session, org_id, spans, args.out / ATTACHMENTS_DIR)
    spans = [
        attachment_refs.rewrite(
            span, lambda reference: {**reference, "key": digests[reference["key"]]}
        )
        for span in spans
    ]

    spans.sort(key=lambda span: ((span.get("metrics") or {}).get("start") or 0))
    with (args.out / LOGS_FILE).open("w") as f:
        for span in spans:
            f.write(json.dumps(span, sort_keys=True) + "\n")

    print(
        f"Wrote {len(spans)} spans and {len(digests)} attachment references "
        f"({len(set(digests.values()))} distinct files) to {args.out}."
    )


if __name__ == "__main__":
    main()
