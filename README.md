# learn-bt

A hands-on course for getting a team productive with Braintrust. It centers on a
small demo agent, the **Sales Assistant**, and a set of exercises that model the
real workflow a team follows to instrument their agent and set up evals for it.

The exercises walk through that workflow end to end: instrumenting the agent with
tracing, monitoring its logs, building datasets and scorers, running evals, and
reviewing results. Each one is a scaled down version of a task a team does with
their own agent, so the reason behind each step stays clear.

## The Sales Assistant agent

The Sales Assistant is a small agent that assists account executives with common
tasks for handling their accounts. 

It has a set of tools and a body of fixture data, which is static data the agent
can look up (accounts, opportunities, and knowledge base documents). Read tools
query the fixtures. All write tools, such as drafting an email or updating a CRM
record, are mocked, so running the agent never touches a real system.

```
agent/
  agent.py      The agent loop and primary entry point for invoking the agent.
  config.py     Runtime config: model, sampling params, prompt, turn limit.
  tools.py      The tools and their schemas (read tools query fixtures; write tools are mocked).
  fixtures.py   Static seed data the read tools look up.
main.py         A REPL for chatting with the agent.
exercises/      The workshop exercises, grouped by section.
```

## Getting started

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
source .venv/bin/activate
```

This demo uses the Braintrust Gateway to handle all model routing. The Gateway allows using any SDK framework with any model, while all model providers are authenticated within Braintrust. This reduces the need for having to maintain provider secrets locally, and also allows us to swap models on the fly without worrying about code changes.

If you do not have access to Braintrust, reach out to an admin in your
organization to get set up.

Set the env vars either in a `.env` file at the repo root:

```bash
cp example.env .env
```

or by exporting them in your shell:

```bash
export BRAINTRUST_API_KEY=sk-...
...
```

### Model routing through the gateway

Model calls are routed to the base URL set by the `BASE_URL` environment
variable, which defaults to the Braintrust AI gateway
(`https://gateway.braintrust.dev`). This
agent uses the OpenAI chat completions API for every provider, and your
`BRAINTRUST_API_KEY` is all that is needed. Model providers should be configured in the Braintrust org, so that provider API keys do not need to be managed in this source code. 

### Running without the gateway

It is possible to go through this course without the Braintrust Gateway. To disable the gateway, set `DISABLE_BRAINTRUST_GATEWAY=1`,
supply an `OPENAI_API_KEY`, and update the `BASE_URL` to OpenAI. Model calls then go directly through the OpenAI provider. In this mode you can
only use OpenAI models, so set the model in `config.py` accordingly.

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
