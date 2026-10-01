# 3.5 Set up a remote eval server

A remote eval server lets domain experts tune an agent and run evals from a
Braintrust playground without touching the code. Developers choose which parts
of the agent configuration to expose as parameters, while the agent and scorer
logic run in a controlled environment.

Any configurable part of the agent can become a parameter, as long as it's a valid Pydantic schema. In this exercise,
you will expose the Sales Assistant's prompt, model, and turn count. The same
pattern can support tool settings, retrieval options, thresholds, or other
configuration that can influence agent quality.

## Step 1: Create the saved parameters

Saved parameters define the controls that a reviewer can change from the
playground. Open `evals/parameters.py`, remove the unused `create_model` import,
and replace the commented-out template with:

~~~python
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
~~~

The prompt parameter renders editable prompt and model controls.
`MaxTurnsParam` exposes the runtime limit without exposing the rest of the agent
configuration.

Push from inside `evals`:

~~~bash
cd evals
bt functions push parameters.py --env-file ../.env
~~~

In Braintrust, confirm that the prompt, model, and maximum-turn controls are visible in the **Parameters** tab.

## Step 2: Write the remote eval task

Open **evals/eval_agent_remote_server.py**. Add these imports below the path setup:

~~~python
from braintrust import Eval, load_parameters

from agent.agent import InputFile, run_agent
from agent.config import AgentConfig
from scorers import recipient_matches_crm

PROJECT = "learn-bt"
saved_parameters = load_parameters(project=PROJECT, slug="sales-assistant-parameters")
~~~

Replace the commented-out task and eval template with:

~~~python
def task(input, hooks):
    prompt_param = hooks.parameters["main"]
    system_prompt_messages = [
        message.as_dict() for message in prompt_param.prompt.messages
    ]

    config = AgentConfig(
        model=prompt_param.options.get("model"),
        system_prompt_messages=system_prompt_messages,
        max_turns=hooks.parameters["max_turns"],
    )

    attachments = []
    attachment = input.get("attachment")
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return run_agent(input["prompt"], attachments=attachments, config=config).output


Eval(
    PROJECT,
    data=[],
    task=task,
    scores=[recipient_matches_crm],  # type: ignore
    parameters=saved_parameters,
)
~~~

The playground sends parameter values through `hooks.parameters`. The task acts
as an adapter: it converts those values to the app's `AgentConfig`, runs the
agent, and returns its output. The agent and scorer logic remain versioned in
the repository.

Notice that data is left blank. That's because the dataset will be selected from the playground directly. Any additional scorers selected in the playground will run in addition to those defined here in the server code.

## Step 3: Start and register the server

From the repository root, run:

~~~bash
bt eval evals/eval_agent_remote_server.py --dev --env-file .env
~~~

This command starts the eval server on your machine. Leave it running. In
Braintrust, open **Settings**, then **Remote Evals**. Add a source with:

~~~text
http://localhost:8300
~~~

Test the connection and save the source. Open a playground, select the remote
eval source, choose a dataset, and run it. If all is configured properly, you should see the eval results populate in the playground.

Duplicate the remote eval task in the playground, change one of the parameters and run an eval again. Both experiments will execute side by side with the different parameter sets. How did that change affect quality?

Congratulations! You just implemented a full flywheel for improving an agent's quality!

## Answer key

Compare your completed source files with these answer keys:

- [`evals/parameters.py`](solutions/05-remote-eval-server/evals/parameters.py)
- [`evals/eval_agent_remote_server.py`](solutions/05-remote-eval-server/evals/eval_agent_remote_server.py)
