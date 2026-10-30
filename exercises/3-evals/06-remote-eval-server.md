# 3.6 Set up a remote eval server

You improved recipient selection by changing the agent's tool configuration in
code. Running those experiments has required a developer. A remote eval server
makes the same process accessible to domain experts. Developers expose selected
configuration, and reviewers run the actual agent from a Braintrust playground
with the existing dataset and scorers.

For our agent, the system prompt messages, model, and max tool call count are the tunable config, so in this exercise we will expose those as parameters.

## Step 1: Define the parameters inline

Parameters define the controls that a reviewer can change from the playground. Any valid Pydantic schema can be exposed as a parameter. Additionally, there are two special parameter types: `prompt` and `model`, which render special UI for configuring those. The `prompt` parameter also includes a model picker.
Open **evals/eval_agent_remote_server.py**. Add these imports and definitions
below the path setup:

~~~python
import uuid

from braintrust import Eval, init_function
from pydantic import BaseModel, Field

from agent.agent import Agent, InputFile
from agent.config import AgentConfig, DEFAULT_CONFIG

PROJECT = "learn-bt"


class MaxToolCallsParam(BaseModel):
    value: int = Field(
        default=DEFAULT_CONFIG.max_tool_calls,
        description="The most tool calls the agent may make to answer one customer message.",
    )


parameters = {
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
    "max_tool_calls": MaxToolCallsParam,
}
~~~

The prompt parameter renders controls for editing the prompt and model.
`MaxToolCallsParam` exposes the runtime limit for tool allowed tool calls, and is defined as a simple Pydantic type. Pass this definition to `Eval(parameters=...)`. See the
[remote eval docs](https://docs.braintrust.dev/evaluate/remote-evals) for further reading.

## Step 2: Write the remote eval task

Next we will wire up the remote eval server. The code here is nearly identical to that of `eval_agent.py` with the addition of exposing the parameters and ingesting them in the task.

~~~python
recipient_matches_crm = init_function(PROJECT, "recipient-matches-crm")
email_quality_scorer = init_function(PROJECT, "email-quality")


async def email_quality(trace, **kwargs):
    tool_spans = await trace.get_spans(span_type=["tool"])
    draft = next(
        (
            span for span in tool_spans
            if span.span_attributes["name"] == "draft_email"
        ),
        None,
    )
    if not draft:
        return None

    return email_quality_scorer(output=draft.output["email"])

def task(input, hooks):
    prompt_param = hooks.parameters["main"]
    system_prompt_messages = [
        message.as_dict() for message in prompt_param.prompt.messages
    ]

    config = AgentConfig(
        model=prompt_param.options.get("model"),
        system_prompt_messages=system_prompt_messages,
        max_tool_calls=hooks.parameters["max_tool_calls"],
    )

    attachments = []
    attachment = input.get("attachment")
    if attachment is not None:
        attachments.append(InputFile.from_dataset_attachment(attachment))

    return Agent(config).chat_turn(
        input["prompt"],
        session_id=uuid.uuid4().hex,
        attachments=attachments,
        history=input.get("history"),
    ).output


Eval(
    PROJECT,
    data=[],
    task=task,
    scores=[recipient_matches_crm, email_quality],  # type: ignore
    parameters=parameters,
)
~~~

The task converts `hooks.parameters` from the playground into an `AgentConfig` definition and runs our agent with this config. This allows for iterating on these parameters from the Braintrust UI by domain experts, and executing the eval remotely on our server with the updated parameters.

`data=[]` is ignored for a remote eval because it will be selected from the playground. Scorers selected there run alongside those defined in the server.

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

Ensure the connection works and save the source. Open a playground, select the remote eval source, and choose **crm-recipient-mismatches** as the dataset. The initially loaded config parameters will be the defaults defined in our config code.

## Step 4: Compare an email-writing prompt variant

Duplicate the task in the playground to run a side by side comparison. Keep the model and tool-call limit the same so this experiment
changes only the prompt.

Read the email-quality failures and their explanations. Add guidance to the candidate's system prompt that addresses the recurring issue. You can use Loop to iterate on the prompt here. Example addition to the prompt:

~~~text
When drafting customer emails:
- Produce a complete subject and body with no placeholders or template text.
  If sender details are unavailable, omit the sender signature.
- Keep the body concise, aiming for 150 words or fewer. Use short paragraphs
  and remove generic opening pleasantries and repetition.
- Write in a professional, conversational tone: friendly, direct, and respectful.
  Avoid stiff language, slang, excessive enthusiasm, and emojis.
- Use a clear, specific subject.
~~~

Run both variants and compare them side by side. Keep the judge's rubric fixed.
Check whether **email_quality** improves, read the actual drafts and explanations,
and confirm **Recipient matches CRM** remains strong. If the candidate does not
improve the drafts, revise it based on the evidence and compare again. Record
which configuration you would choose and why. A domain expert can now conduct
this experiment without modifying Python files.

## Step 5: Apply the chosen configuration

If the candidate improves the drafts without reducing recipient correctness,
copy its complete system prompt into `SYSTEM_PROMPT` in **agent/config.py**.
Otherwise, try iterating further using Loop.

## Answer key

Compare your completed
[evals/eval_agent_remote_server.py](solutions/06-remote-eval-server/evals/eval_agent_remote_server.py)
with this answer key.
