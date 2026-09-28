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
| 0 | `0-foundations` | Get oriented in Braintrust and the CLI |
| 1 | `1-instrumentation` | Add tracing to the agent |
| 2 | `2-active-observability` | Inspect production traffic with SQL, Loop, Topics, and Debugger |
| 3 | `3-evals` | Turn a Loop finding into a regression dataset, baseline, and fix |
| 4 | `4-human-review` | Custom views, human review, remote evals |

Each exercise is a markdown file with a task, and occasionally a short bit of
background. Exercises that require source changes include a `solutions/` folder
with the completed source files. UI-only exercises do not have an answer key.

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
