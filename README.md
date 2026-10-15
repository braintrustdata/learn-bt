# learn-bt

A hands-on Braintrust course using a demo **Sales Assistant** agent. The
exercises follow an email-quality investigation: add tracing, inspect logs,
build datasets and scorers, run evals, and compare improvements.

## The Sales Assistant agent

The Sales Assistant helps account executives research accounts, draft emails,
and update CRM records. Its read tools query static accounts, opportunities,
and knowledge-base documents. Email drafting and CRM updates are mocked; they
do not send email or change real records.

```
agent/
  agent.py      The demo agent
  config.py     The agent's runtime config
  tools.py      The tools and their schemas
  fixtures.py   Static seed data the read tools look up.
main.py         A REPL for chatting with the agent.
exercises/      The workshop exercises, grouped by section.
```

See the [exercises overview](exercises/README.md) for the course sequence.

## Getting started

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
source .venv/bin/activate
```

If you do not have access to Braintrust, reach out to an admin in your
organization to get set up.

Copy the environment template to `.env` at the repo root, then fill in its values:

```bash
cp example.env .env
```

Alternatively, export the variables in your shell:

```bash
export BRAINTRUST_API_KEY=sk-...
...
```

### Model routing through the gateway

Set `BASE_URL` to `https://gateway.braintrust.dev` to route model calls through
the Braintrust Gateway. The agent uses the OpenAI chat completions API across
providers. Configure provider credentials in your Braintrust org; locally, the
agent authenticates with `BRAINTRUST_API_KEY`. You can then switch models
without changing the client code.

### Running without the gateway

To use OpenAI directly, set `DISABLE_BRAINTRUST_GATEWAY=1`, supply an
`OPENAI_API_KEY`, and set `BASE_URL` to OpenAI. Choose an OpenAI model in
`agent/config.py`.

```bash
DISABLE_BRAINTRUST_GATEWAY=1
OPENAI_API_KEY=sk-...
BASE_URL="https://api.openai.com/v1"
```

Once the key (and base URL, if you changed it) is set, start the REPL and chat
with the agent:

```bash
uv run python main.py
```
