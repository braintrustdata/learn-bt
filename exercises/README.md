# Exercises

Hands-on exercises for the Braintrust enablement workshop. Each one is a scaled
down version of a real workflow, applied to the Sales Assistant agent in this
repo. You start with a plain, uninstrumented agent. By the end you have an agent
that is fully traced, queried, evaluated, and set up for human and remote review.

## How the exercises are organized

Exercises are grouped into sections that match the workshop content.

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

## What to expect in each exercise

Each exercise introduces a problem or concept and walks through the steps to
solve it and inspect the result. Prerequisites identify the data, code, or saved
artifacts needed for the task. Answer keys support code exercises; linked
documentation provides optional further reading.

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
