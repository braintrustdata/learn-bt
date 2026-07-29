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

Requires BRAINTRUST_API_KEY (a .env file is loaded if present). All model calls
route through the Braintrust gateway, so no provider-specific key is needed.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import textwrap
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

# Each fixture kind gets a short framing of what an AE would be doing with it, so
# the generated request reads like a real ask rather than a bare data dump.
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the Sales Assistant with traffic.")
    parser.add_argument("--count", type=int, default=10, help="Number of traces to seed.")
    parser.add_argument("--attachment-ratio", type=float, default=0.2,
                        help="Fraction of requests that include an attachment (0-1).")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model used to generate requests.")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed for reproducibility.")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    # Routes through the Braintrust gateway, same as the agent, so only
    # BRAINTRUST_API_KEY is required.
    client = OpenAI(
        base_url="https://gateway.braintrust.dev",
        api_key=os.environ["BRAINTRUST_API_KEY"],
    )

    print(f"Generating and running {args.count} requests...")
    for i in range(1, args.count + 1):
        fixture_kind = rng.choice(list(FIXTURE_KINDS))
        fixtures = FIXTURE_KINDS[fixture_kind][0]
        fixture = rng.choice(list(fixtures.values()))
        with_attachment = rng.random() < args.attachment_ratio

        try:
            req = _generate_request(client, args.model, fixture_kind, fixture, with_attachment)
        except Exception as exc:  # keep seeding even if generation fails
            print(f"[{i}/{args.count}] generation failed: {exc}")
            continue

        prompt = req.get("prompt", "")
        attachments : list[str | Path] | None = None
        if with_attachment and req.get("attachment_text"):
            attachments = [render_attachment(req["attachment_text"], i)]

        label = "with attachment" if attachments else "text only"
        print(f"[{i}/{args.count}] ({fixture_kind}, {label}) {prompt[:70]}")
        try:
            result = run_agent(prompt, attachments=attachments)
            for write in result.writes:
                print(f"    side effect: {write['action']}")
        except Exception as exc:  # keep seeding even if one run fails
            print(f"    run failed: {exc}")

    print("Done. If the agent is instrumented, check your Braintrust project logs.")


if __name__ == "__main__":
    main()
