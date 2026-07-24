# learn-bt: Braintrust enablement workshop

A hands-on course for getting a team productive on Braintrust. It centers on one
small agent, the **Sales Assistant**, and a set of exercises that take it from
uninstrumented code to a fully traced, evaluated, and reviewable system.

The exercises are organized around the problems observability and evals solve
(instrument, monitor, evaluate, review), not around product features. Each
exercise is a scaled down version of a real workflow applied to the agent, so the
"why" is always clear.

## The agent

The Sales Assistant helps an account team prepare for and follow up on customer
conversations. It is deliberately simple so the focus stays on instrumentation and
evaluation.

```
agent/
  config.py     Tunable runtime config: model, sampling params, prompt messages
                (OpenAI chat schema), and tool descriptions. This is what later
                becomes remote-eval parameters.
  tools.py      The tools: lookup_customer, get_opportunity, search_knowledge_base,
                draft_email (mock), update_crm_record (mock).
  fixtures.py   In-memory seed data the tools read (accounts, opportunities, docs).
  agent.py      Builds the Pydantic AI agent from the config and runs it. Supports
                file attachments. Starts with no tracing on purpose.
main.py         A REPL for chatting with the agent.
scripts/seed.py Generates realistic requests and runs the agent to seed traces.
evals/          Eval files: scorer and eval templates you complete, plus
                reference dataset pipeline and remote eval server.
exercises/      The workshop exercises, grouped by section.
```

### Model routing

All model calls go through the **Braintrust AI gateway**, an OpenAI-compatible
endpoint. That means a single `BRAINTRUST_API_KEY` reaches every provider, and you
can change the model in `config.py` (`gpt-4o-mini`, `claude-3-5-sonnet-latest`,
`gemini-2.5-flash`, ...) with no new credentials. No OpenAI or Anthropic key is
needed.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
echo "BRAINTRUST_API_KEY=sk-..." > .env
```

## Try it

```bash
# Chat with the agent
uv run python main.py

# Seed a batch of traces (populates Braintrust once the agent is instrumented)
uv run python -m scripts.seed --count 20 --attachment-ratio 0.3
```

## The workshop

Work through the exercises in order. Each section builds on the state you left the
agent in. See [`exercises/README.md`](exercises/README.md) for the full map.

| Section | Folder | You will |
| --- | --- | --- |
| 1 Foundations | `exercises/0-foundations` | Explore a seeded project and set up the CLI |
| 2 Instrumentation | `exercises/1-instrumentation` | Add tracing and log attachments |
| 3 Monitoring | `exercises/2-monitoring` | Query logs with SQL and analyze them with Loop |
| 4 Evals | `exercises/3-evals` | Curate datasets, build scorers, run and compare evals |
| 5 Human + remote review | `exercises/4-human-review` | Build custom views, run human review, stand up a remote eval |

By the end, the agent you started with is instrumented, its logs are queryable,
its quality is measured by evals, its edge cases are human-reviewed, and its
config is tunable by non-engineers through a playground.
