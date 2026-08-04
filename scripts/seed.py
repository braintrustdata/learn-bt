"""Seed the agent with realistic traffic.

For each request the script randomly picks a fixture object (an account or an
opportunity), asks an LLM to write the single request an
account executive might type about it, then runs the agent on that request. Once
you have instrumented the agent with Braintrust tracing (section 2), running this
populates your project's logs with varied traces you can query, cluster, and
analyze in later sections.

Some requests arrive with an attachment: the LLM also drafts a short "customer
message", which the script renders as either a text PDF or a PNG and passes to
the agent as input, so you have traces that exercise attachment logging.

Usage:
    uv run python -m scripts.seed --count 20
    uv run python -m scripts.seed --count 20 --attachment-ratio 0.3
    uv run python -m scripts.seed --count 20 --concurrency 4

Requires BRAINTRUST_API_KEY (a .env file is loaded if present). All model calls
route through the Braintrust gateway, so no provider-specific key is needed.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from agent.agent import run_agent
from agent.fixtures import ACCOUNTS, OPPORTUNITIES

load_dotenv()

SCRATCH_DIR = Path(__file__).parent / ".seed_attachments"

FIXTURE_KINDS = {
    "account": (
        ACCOUNTS,
        "You need to do something with this CRM account (review it, update a "
        "field, prep for a call, draft an email to the contact, etc.).",
    ),
    "opportunity": (
        OPPORTUNITIES,
        "You are working this opportunity and want to move it forward (check its "
        "status, update the next step, draft an update, ask what to do next, etc.).",
    ),
}

GENERATOR_SYSTEM = """You generate a realistic request that an account
executive would type to a Sales Assistant agent. The agent can look up accounts
and opportunities, search a knowledge base, draft emails, and update CRM records.

You are given one piece of context the AE is currently focused on. Write the
request as if the AE has that context in front of them: they can reference it by
name or id, and their ask should plausibly require the assistant to look it up or
act on it. Keep it to one or two sentences and make it sound like a busy person
typing quickly.

An AE may share an attachment along with their request too. An attachment can be a pdf file or an image. When asked to generate an attachment, generate the text content of that attachment, and make it relevant to the actual prompt the AE would give the agent. Ex. the AE may ask to update something in CRM for an account, and share a screenshot of a message from the customer asking for a renewal.

Return a JSON object with:
  - "prompt": the AE's request (one or two sentences).
  - "attachment_text": when asked to include an attachment, generate content for
  that attachment here. This attachment will be a customer message. Make it relevant 
  to the prompt context; otherwise null.
"""


def _generate_request(
    client: OpenAI, model: str, fixture_kind: str, fixture: dict, with_attachment: bool
) -> dict:
    """Ask the LLM for one request grounded in a single fixture object."""
    _, framing = FIXTURE_KINDS[fixture_kind]
    attachment_clause = (
        "The AE is forwarding a customer message, so include attachment_text."
        if with_attachment
        else "No attachment for this one; set attachment_text to null."
    )
    instruction = textwrap.dedent(
        f"""Generate a request. Context ({fixture_kind}): {framing}

        Here are the details:
        {json.dumps(fixture, indent=2)}

        {attachment_clause}"""
    )
    resp = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": GENERATOR_SYSTEM},
            {"role": "user", "content": instruction},
        ],
    )
    return json.loads(resp.choices[0].message.content or "{}")


def _render_pdf(text: str, path: Path) -> None:
    """Render a customer message as a real (text-based, selectable) PDF."""
    c = canvas.Canvas(str(path), pagesize=LETTER)
    width, height = LETTER
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, "Customer message")
    c.setFont("Helvetica", 12)
    y = height - inch - 0.5 * inch
    for line in textwrap.wrap(text, width=80):
        c.drawString(inch, y, line)
        y -= 0.28 * inch
    c.showPage()
    c.save()


def _render_png(text: str, path: Path) -> None:
    """Draw a short customer message onto a PNG image."""
    width, height = 600, 320
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, 40], fill=(37, 99, 235))
    draw.text((16, 12), "Customer message", fill="white")
    draw.text((16, 60), textwrap.fill(text, width=64), fill=(20, 20, 20))
    img.save(path)


def render_attachment(text: str, index: int) -> Path:
    """Render a customer message as an attachment, alternating PDF and PNG.

    Later exercises log both text (PDF) and image (PNG) attachments, so the seed
    set includes both formats.
    """
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    if index % 2 == 0:
        path = SCRATCH_DIR / f"message_{index:02d}.pdf"
        _render_pdf(text, path)
    else:
        path = SCRATCH_DIR / f"message_{index:02d}.png"
        _render_png(text, path)
    return path


def _seed_one(
    client: OpenAI, args: argparse.Namespace, fixture_kind: str, fixture: dict,
    with_attachment: bool, i: int, total: int,
) -> None:
    """Generate a single request and run the agent on it."""
    try:
        req = _generate_request(client, args.model, fixture_kind, fixture, with_attachment)
    except Exception as exc:  # keep seeding even if generation fails
        print(f"[{i}/{total}] generation failed: {exc}")
        return

    prompt = req.get("prompt", "")
    attachments : list[Path] = []
    if with_attachment and req.get("attachment_text"):
        attachments = [render_attachment(req["attachment_text"], i)]

    label = "with attachment" if attachments else "text only"
    print(f"[{i}/{total}] ({fixture_kind}, {label}) {prompt}")
    try:
        run_agent(prompt, attachments=attachments)
    except Exception as exc:  # keep seeding even if one run fails
        print(f"    run failed: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the Sales Assistant with traffic.")
    parser.add_argument("--count", type=int, default=10, help="Number of traces to seed.")
    parser.add_argument("--attachment-ratio", type=float, default=0.2,
                        help="Fraction of requests that include an attachment (0-1).")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model used to generate requests.")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed for reproducibility.")
    parser.add_argument("--concurrency", type=int, default=1,
                        help="Number of requests to generate and run concurrently.")
    args = parser.parse_args()

    if args.concurrency < 1:
        parser.error("--concurrency must be at least 1")

    rng = random.Random(args.seed)

    if os.environ.get("DISABLE_BRAINTRUST_GATEWAY"):
        client = OpenAI(
            base_url=os.environ["BASE_URL"]
        )
    else:
        client = OpenAI(
            base_url=os.environ["BASE_URL"],
            api_key=os.environ["BRAINTRUST_API_KEY"],
        )

    # Draw all random choices up front on the single RNG so that a given --seed
    # produces the same workload regardless of --concurrency.
    jobs = []
    for i in range(1, args.count + 1):
        fixture_kind = rng.choice(list(FIXTURE_KINDS))
        fixtures = FIXTURE_KINDS[fixture_kind][0]
        fixture = rng.choice(list(fixtures.values()))
        with_attachment = rng.random() < args.attachment_ratio
        jobs.append((fixture_kind, fixture, with_attachment, i))

    print(f"Generating and running {args.count} requests "
          f"({args.concurrency} at a time)...")
    if args.concurrency == 1:
        for fixture_kind, fixture, with_attachment, i in jobs:
            _seed_one(client, args, fixture_kind, fixture, with_attachment, i, args.count)
    else:
        with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            futures = [
                executor.submit(
                    _seed_one, client, args, fixture_kind, fixture, with_attachment, i, args.count
                )
                for fixture_kind, fixture, with_attachment, i in jobs
            ]
            for future in as_completed(futures):
                future.result()

    print("Done. If the agent is instrumented, check your Braintrust project logs.")


if __name__ == "__main__":
    main()
