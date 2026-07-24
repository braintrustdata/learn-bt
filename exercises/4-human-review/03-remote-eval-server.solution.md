# Solution: Set up a remote eval server

References: [`evals/parameters.py`](../../evals/parameters.py) and
[`evals/eval_remote_agent.py`](../../evals/eval_remote_agent.py).

## 1. Parameters (`evals/parameters.py`)

```python
import braintrust
from pydantic import BaseModel, Field

from agent.config import DEFAULT_CONFIG, SYSTEM_PROMPT

project = braintrust.projects.create(name="sales-assistant")


class TemperatureParam(BaseModel):
    value: float = Field(default=DEFAULT_CONFIG.params.temperature)


project.parameters.create(
    name="Sales Assistant config",
    slug="sales-assistant-config",
    description="Tunable configuration for the Sales Assistant agent.",
    schema={
        "model": {
            "type": "model",
            "default": DEFAULT_CONFIG.model,
            "description": "Model to run the agent with.",
        },
        "temperature": TemperatureParam,
        "system_prompt": {
            "type": "prompt",
            "description": "System prompt that steers the agent.",
            "default": {
                "prompt": {
                    "type": "chat",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": "{{input}}"},
                    ],
                },
                "options": {"model": DEFAULT_CONFIG.model},
            },
        },
    },
)
```

Push with `cd evals && bt functions push parameters.py`. `type: "model"` renders a
model dropdown, and `type: "prompt"` renders an editable prompt. Braintrust seeds
the first version with these defaults, so the parameters are immediately editable
in the UI.

## 2. Remote eval server (`evals/eval_remote_agent.py`)

```python
from braintrust import Eval, init_dataset, load_parameters
from autoevals import Factuality

from agent.agent import run_agent
from agent.config import AgentConfig, Message, ModelParams

PROJECT = "sales-assistant"

saved_parameters = load_parameters(project=PROJECT, slug="sales-assistant-config")


def task(input: str, hooks) -> str:
    params = hooks.parameters

    built = params["system_prompt"].build(input=input)
    system_prompt = "\n\n".join(
        m["content"] for m in built["messages"] if m["role"] == "system"
    )

    config = AgentConfig(
        model=params["model"],
        params=ModelParams(temperature=params["temperature"]),
        messages=[Message(role="system", content=system_prompt)],
    )
    return run_agent(input, config=config).output


Eval(
    PROJECT,
    data=init_dataset(project=PROJECT, name="sales-assistant-eval"),
    task=task,
    scores=[Factuality()],
    parameters=saved_parameters,
)
```

## 3. Run

```bash
bt eval evals/eval_remote_agent.py --dev
```

Register the local dev server in a playground, then run the eval. Each parameter
appears as a control.

## Notes

- Because the agent is built config-first, the UI parameters map straight onto an
  `AgentConfig`. The same fields a developer edits in `config.py` are the ones an
  SME now tunes from the playground.
- `hooks.parameters["model"]` and `["temperature"]` return the values directly.
  The `prompt` parameter returns a prompt object, so call `.build(input=...)` and
  read the system message out of the result. The agent adds the user input itself,
  so the `{{input}}` user message in the prompt is just for the playground preview.
- The dev server is HTTP and its health check is public, though the eval endpoints
  require your API key. For anything beyond local use, restrict with
  `--dev-org-name` and put it behind HTTPS.
