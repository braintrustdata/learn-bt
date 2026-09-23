# 4.3 Set up a remote eval server

Expose the Sales Assistant configuration as saved parameters, then run the agent locally from a Braintrust Playground. This lets reviewers compare prompt, model, and turn-limit changes without editing code for every trial.

## Step 1: Create the saved parameters

Open **evals/parameters.py**. Remove the unused **create_model** import. Replace the commented-out template with:

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

The prompt parameter renders an editable prompt and model control. **MaxTurnsParam** exposes a separate runtime safety limit.

Push from inside **evals**:

~~~bash
cd evals
bt functions push parameters.py --env-file ../.env
~~~

In Braintrust, confirm that the prompt, model, and maximum-turn controls are editable.

## Step 2: Write the remote eval task

Open **evals/eval_agent_remote_server.py**. Add these imports below the path setup:

~~~python
from braintrust import Eval, load_parameters

from agent.agent import InputFile, run_agent
from agent.config import AgentConfig
from scorers import email_goal_reached, valid_email

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
    scores=[valid_email, email_goal_reached],  # type: ignore
    parameters=saved_parameters,
)
~~~

The Playground sends parameter values through **hooks.parameters**. The task converts those values to the app's **AgentConfig**, while the agent and scorers remain version-controlled locally.

## Step 3: Start and register the server

From the repository root, run:

~~~bash
bt eval evals/eval_agent_remote_server.py --dev --env-file .env
~~~

Leave that command running. In Braintrust, open **Settings**, then **Remote Evals**. Register a source with:

~~~text
http://localhost:8300
~~~

Test the connection and save the source. Open a Playground, select the remote eval source, choose a dataset, and run it. The agent runs locally while results and parameter changes remain visible in Braintrust.

## Solution

See [03-remote-eval-server.solution.md](03-remote-eval-server.solution.md).
