# Exercises

These exercises use the Sales Assistant to practice tracing, investigating
failures, and evaluating changes. You start with an uninstrumented agent and
add tracing, human review, regression evals, and a remote eval server.

## How the exercises are organized

| Section | Folder | Theme |
| --- | --- | --- |
| 0 | `0-setup` | Configure the environment and meet the agent |
| 1 | `1-instrumentation` | Add tracing and a custom view to the agent |
| 2 | `2-active-observability` | Inspect production traffic with search, SQL, Topics, Loop, and Debugger |
| 3 | `3-evals` | One regression dataset, scorers, human review, baselines, fixes, and remote iteration |

Exercises that require source changes include completed files in a
`solutions/` folder.

## The investigation

You own a Sales Assistant that account executives are using, but you cannot yet
explain its behavior. Add tracing, understand production-like traffic, and
investigate customer email failures. Preserve those failures in one dataset,
measure the current agent, and improve it. Finally, let an account-team expert
compare configuration changes through a remote eval server.

## Prerequisites

Follow the [repository setup instructions](../README.md) to configure credentials.

Install dependencies once from the repo root:

```bash
uv sync
```

## The base agent

The agent lives in `agent/`. It is a Sales Assistant that can look up accounts and
opportunities, search a knowledge base, draft emails, and update CRM records.
See the top-level [README](../README.md) for a tour.
