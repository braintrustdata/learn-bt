"""Seed the agent with realistic traffic.

This script generates a set of realistic Sales Assistant requests with an LLM,
then runs the agent on each one. Once you have instrumented the agent with
Braintrust tracing (section 2), running this populates your project's logs with
varied traces you can query, cluster, and analyze in later sections.

Some requests arrive with an attachment: the script renders a short "customer
message" into a PNG and passes it to the agent as multimodal input, so you have
traces that exercise attachment logging.

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
import textwrap
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image, ImageDraw

from agent.agent import run_agent

load_dotenv()

SCRATCH_DIR = Path(__file__).parent / ".seed_attachments"

# A compact description of what lives in the fixtures, so the generator produces
# requests that actually hit the tools instead of asking about unknown accounts.
FIXTURE_CONTEXT = """
Accounts: Northwind Trading (ACC-1001, logistics, EU expansion, data residency),
Halcyon Health (ACC-1002, healthcare, needs HIPAA), Bright Peak Media (ACC-1003,
media, champion left).
Opportunities: OPP-5001 (Northwind EU expansion, Negotiation), OPP-5002 (Halcyon
upsell, Proposal), OPP-5003 (Bright Peak renewal, Discovery).
Knowledge base covers: pricing and discounts, security/HIPAA/data residency,
onboarding timelines, competitive positioning.
"""

GENERATOR_SYSTEM = """You generate realistic requests that an account executive
would type to a Sales Assistant agent. The agent can look up accounts and
opportunities, search a knowledge base, draft emails, and update CRM records.

Return a JSON object with a "requests" array. Each item has:
  - "prompt": the AE's request (one or two sentences).
  - "needs_attachment": boolean. True for a few requests where the AE forwards a
    customer message.
  - "attachment_text": if needs_attachment is true, the short customer message to
    render as an image (2-4 sentences); otherwise null.

Make the set diverse: some reference specific accounts or opportunities, some ask
for emails to be drafted, some ask about pricing or security. Include a couple of
vague or underspecified requests so the agent has to cope with ambiguity.
"""


def generate_requests(count: int, attachment_ratio: float, model: str) -> list[dict]:
    """Ask an LLM for `count` realistic requests grounded in the fixtures."""
    # Routes through the Braintrust gateway, same as the agent, so only
    # BRAINTRUST_API_KEY is required.
    client = OpenAI(
        base_url="https://gateway.braintrust.dev",
        api_key=os.environ["BRAINTRUST_API_KEY"],
    )
    instruction = textwrap.dedent(
        f"""Generate {count} requests. About {round(attachment_ratio * 100)}% should
        set needs_attachment to true. Ground them in this data:
        {FIXTURE_CONTEXT}"""
    )
    resp = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": GENERATOR_SYSTEM},
            {"role": "user", "content": instruction},
        ],
    )
    data = json.loads(resp.choices[0].message.content or "{}")
    requests = data.get("requests", [])
    return requests[:count]


def _render_message(text: str) -> Image.Image:
    """Draw a short customer message onto an image."""
    width, height = 600, 320
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, 40], fill=(37, 99, 235))
    draw.text((16, 12), "Customer message", fill="white")
    draw.text((16, 60), textwrap.fill(text, width=64), fill=(20, 20, 20))
    return img


def render_attachment(text: str, index: int) -> Path:
    """Render a customer message as an attachment, alternating PNG and PDF.

    Later exercises log both image and PDF attachments, so the seed set includes
    both formats.
    """
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    img = _render_message(text)
    if index % 2 == 0:
        path = SCRATCH_DIR / f"message_{index:02d}.pdf"
        img.save(path, "PDF", resolution=100.0)
    else:
        path = SCRATCH_DIR / f"message_{index:02d}.png"
        img.save(path)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the Sales Assistant with traffic.")
    parser.add_argument("--count", type=int, default=10, help="Number of traces to seed.")
    parser.add_argument("--attachment-ratio", type=float, default=0.2,
                        help="Fraction of requests that include an attachment (0-1).")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model used to generate requests.")
    args = parser.parse_args()

    print(f"Generating {args.count} requests...")
    requests = generate_requests(args.count, args.attachment_ratio, args.model)

    for i, req in enumerate(requests, start=1):
        prompt = req.get("prompt", "")
        attachments = None
        if req.get("needs_attachment") and req.get("attachment_text"):
            attachments = [render_attachment(req["attachment_text"], i)]

        label = "with attachment" if attachments else "text only"
        print(f"[{i}/{len(requests)}] ({label}) {prompt[:70]}")
        try:
            result = run_agent(prompt, attachments=attachments)
            for write in result.writes:
                print(f"    side effect: {write['action']}")
        except Exception as exc:  # keep seeding even if one run fails
            print(f"    run failed: {exc}")

    print("Done. If the agent is instrumented, check your Braintrust project logs.")


if __name__ == "__main__":
    main()
