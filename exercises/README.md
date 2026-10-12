# Exercises

Hands-on exercises for the Braintrust enablement workshop. Each one is a scaled
down version of a real workflow, applied to the Sales Assistant agent in this
repo. You start with a plain, uninstrumented agent. By the end you have an agent
that is fully traced, queried, evaluated, and set up for human and remote review.

## How the exercises are organized

Exercises are grouped into sections that match the workshop content. Work through
them in order. Each later section builds on the state you left the agent in.

| Section | Folder | Theme |
| --- | --- | --- |
| 0 | `0-setup` | Configure the environment and meet the agent |
| 1 | `1-instrumentation` | Add tracing and a custom view to the agent |
| 2 | `2-active-observability` | Inspect production traffic with search, SQL, Topics, Loop, and Debugger |
| 3 | `3-evals` | Human review, one regression dataset, scorers, baselines, fixes, and remote iteration |

Each exercise is a markdown file with a task, and occasionally a short bit of
background. Exercises that require source changes include a `solutions/` folder
with the completed source files. UI-only exercises do not have an answer key.

## The course story

You own a Sales Assistant that account executives are using, but you cannot yet
explain its behavior. Add tracing, understand production-like traffic, and
investigate customer email failures. Preserve those failures in one dataset,
measure the current agent, and improve it. Finally, let an account-team expert
compare configuration changes through a remote eval server.

## Exercise sequence

- **Setup:** [environment](0-setup/01-setup-braintrust-cli.md), then
  [assignment](0-setup/02-meet-the-agent.md).
- **Instrumentation:** [tracing](1-instrumentation/01-instrument-tracing.md),
  [attachments](1-instrumentation/02-log-attachments.md), and
  [review view](1-instrumentation/03-custom-view.md).
- **Active observability:** [search and SQL](2-active-observability/01-sql-querying.md),
  [usage with Topics](2-active-observability/02-topics.md),
  [failure discovery with Loop](2-active-observability/03-loop.md), and
  [debugging an email failure](2-active-observability/04-debug-a-trace.md).
- **Evals:** [human review](3-evals/01-human-review-intake.md),
  [regression dataset](3-evals/02-curating-datasets.md),
  [scorers](3-evals/03-creating-scorers.md),
  [baseline](3-evals/04-executing-an-eval.md),
  [recipient fix](3-evals/05-fix-recipient-selection.md), and
  [remote iteration](3-evals/06-remote-eval-server.md).

## Prerequisites

- Check out the README.md at root for getting started.

Install dependencies once from the repo root:

```bash
uv sync
```

## The base agent

The agent lives in `agent/`. It is a Sales Assistant that can look up accounts and
opportunities, search a knowledge base, draft emails, and update CRM records. It
is intentionally small so you can focus on instrumentation and evaluation rather
than on understanding the agent. See the top-level `README.md` for a tour.
