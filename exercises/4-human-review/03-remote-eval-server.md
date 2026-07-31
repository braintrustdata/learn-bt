# 5.3 Set up a remote eval server

Expose the agent's config as parameters so it can be tuned from a playground,
without touching code. A remote eval loads a saved parameters object and runs
locally while the UI drives it.

## Task

### 1. Create and push a parameters object

In `evals/parameters.py`, build a parameters object from the agent's `config.py`.
Use a `prompt` parameter for the system prompt so it gets an editable prompt
control in the UI; the prompt parameter also carries the model name.

Push these parameters to Braintrust via:

```bash
cd evals
bt functions push parameters.py
```

Verify in the UI that the parameters appear and are editable.

### 2. Write the remote eval server

In `evals/eval_remote_agent.py`, load the parameters and pass their values down
through the `hooks` object to build an `AgentConfig` and run the agent. Follow the attachment reading pattern implemented in the previous eval exercise.

### 3. Run it

Start the dev server, open a playground, and execute an eval:

```bash
bt eval evals/eval_remote_agent.py --dev
```

In Braintrust, register the remote eval server source from Settings -> Remote Evals. Enter the host URL (default: `http://localhost:8300`), test the connection, and save. If all goes well, the server should be accessible in the Braintrust Playground. 

## Solution

See [03-remote-eval-server.solution.md](03-remote-eval-server.solution.md).
