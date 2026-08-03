# Solution: Set up a remote eval server

## 1. Parameters (`evals/parameters.py`)

```python
import braintrust
from pydantic import BaseModel, Field

from agent.config import DEFAULT_CONFIG

project = braintrust.projects.create(name="learn-bt")


class MaxTurnsParam(BaseModel):
    value: int = Field(
        default=DEFAULT_CONFIG.max_turns,
        description="The most model calls a single agent run may make.",
    )


project.parameters.create(
    name="Sales Assistant Parameters",
    slug="sales-assistant-parameters",
    description="Tunable configuration for the Sales Assistant agent.",
    schema={
        "main": {
            "type": "prompt",
            "description": "Agent's main prompt",
            "default": {
                "prompt": {
                    "type": "chat",
                    "messages": DEFAULT_CONFIG.system_prompt_messages,
                },
                "options": {"model": DEFAULT_CONFIG.model},
            },
        },
        "max_turns": MaxTurnsParam,
    },
)
```

Push with `cd evals && bt functions push parameters.py`. `type: "prompt"` renders an editable prompt control that also owns the model dropdown and model parameters. `prompt` is a special parameter type. Parameters can be created for any Pydantic BaseModel, which is how `max_turns` gets a control of its own: the model wraps the value in a `value` field and Braintrust reads the type and description off it.

## 2. Remote eval server (`evals/eval_remote_agent.py`)

```python
import sys
from pathlib import Path

from braintrust import Eval, init_dataset, load_parameters
from autoevals import Factuality

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent.agent import InputFile, run_agent
from agent.config import AgentConfig
from scorers import valid_email, email_goal_reached

PROJECT = "learn-bt"

saved_parameters = load_parameters(project=PROJECT, slug="sales-assistant-parameters")


def task(input, hooks):
    prompt_param = hooks.parameters["main"]
    system_prompt_messages = [message.as_dict() for message in prompt_param.prompt.messages]

    config = AgentConfig(
        model=prompt_param.options.get("model"),
        system_prompt_messages=system_prompt_messages,
        max_turns=hooks.parameters["max_turns"],
    )

    attachment = input.get("attachment")

    # Dataset attachments arrive as ReadonlyAttachment (hydrated by init_dataset)
    attachments = []
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return run_agent(input["prompt"], attachments=attachments, config=config).output


Eval(
    PROJECT,
    data=[],
    task=task,
    scores=[valid_email, email_goal_reached], #type: ignore
    parameters=saved_parameters,
)
```

## 3. Run

```bash
bt eval evals/eval_remote_agent.py --dev
```

Register the local dev server in a playground, then run the eval.

## Notes
- When using a remote eval server as the eval task, the Braintrust UI proxies each request to the server and simply waits for the response. This allows complex eval logic to stay in place, while still providing all users access to the same eval location.
- New parameters iterated on in a playground can be saved as a new version directly from the playground.
- `hooks.parameters["max_turns"]` hands back the plain integer. The `value` field only exists to declare the parameter's type and description; you don't unwrap it at runtime. The `prompt` parameter behaves differently because it is a Braintrust type: it returns a prompt object you read `.prompt.messages` and `.options` off.
- `max_turns` is an ordinary field on `AgentConfig`, and exposing it took a four-line Pydantic model. Any system level configuration that's a valid Pydantic BaseModel can be tuned at eval runtime the same way. As a bonus, add a parameter that restricts which tools the agent is allowed to call.
- The data field in the `Eval()` is ignored for a remote eval. The dataset is selected at runtime. Additional scorers defined in the UI are appended to the eval defined scorers.