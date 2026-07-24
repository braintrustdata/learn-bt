# 5.3 Set up a remote eval server

Expose the agent's config as parameters so it can be tuned from a playground,
without touching code. A remote eval loads a saved parameters object and runs
locally while the UI drives it.

## Task

### 1. Create and push a parameters object

In `evals/parameters.py`, build a parameters object from the agent's `config.py`.
Include the model, the temperature, and the system prompt. Use a `prompt`
parameter for the system prompt so it gets an editable prompt control in the UI.
Push it:

```bash
cd evals
bt functions push parameters.py
```

Verify in the UI that the parameters appear and are editable.

### 2. Write the remote eval server

In `evals/eval_remote_agent.py`, load the parameters and pass their values down
through the `hooks` object to build an `AgentConfig` and run the agent.

### 3. Run it

Start the dev server, open a playground, and execute an eval:

```bash
bt eval evals/eval_remote_agent.py --dev
```

## Solution

See [03-remote-eval-server.solution.md](03-remote-eval-server.solution.md).
