"""Interactive REPL for the Sales Assistant agent.

Run with:

    uv run python main.py

Type a request and the agent responds. To send a file (for example a PDF a
customer emailed you), stage it first with:

    /attach path/to/file.pdf

The file is attached to your next message and then cleared. Type /exit to quit.

Requires BRAINTRUST_API_KEY in your environment (a .env file is loaded if
present). Model calls route through the Braintrust gateway, unless
DISABLE_BRAINTRUST_GATEWAY is set, in which case they go to the OpenAI provider directly
"""

from dotenv import load_dotenv

from agent.agent import run_agent

load_dotenv()

BANNER = """Sales Assistant (type /exit to quit, /attach <path> to attach a file)
"""


def main() -> None:
    print(BANNER)
    pending_attachments: list[str] = []

    while True:
        try:
            line = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue
        if line in ("/exit", "/quit"):
            break
        if line.startswith("/attach "):
            path = line[len("/attach ") :].strip()
            pending_attachments.append(path)
            print(f"(attached {path}; it will be sent with your next message)")
            continue

        result = run_agent(line, attachments=pending_attachments or None)
        pending_attachments = []

        print(f"\nassistant> {result.output}\n")


if __name__ == "__main__":
    main()
