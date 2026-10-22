# 3.6 Set up a remote eval server

You improved recipient selection by changing the agent's tool configuration in
code. Running those experiments has required a developer. A remote eval server
makes the same process accessible to domain experts. Developers expose selected
configuration, and reviewers run the actual agent from a Braintrust playground
with the existing dataset and scorers.

In this exercise, expose the system prompt, model, and maximum tool-call count.
Then take the role of an account-team expert and compare prompt variants that
address the email-writing failures from human review and the baseline. The agent
and scorer logic remain in your repository.

## Step 1: Create the saved parameters

Saved parameters define the controls that a reviewer can change from the
playground. Open `evals/parameters.py`, remove the unused `create_model` import,
and replace the commented-out template with:

~~~python
project = braintrust.projects.create(name="learn-bt")


class MaxToolCallsParam(BaseModel):
    value: int = Field(
        default=DEFAULT_CONFIG.max_tool_calls,
        description="The most tool calls the agent may make to answer one customer message.",
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
        "max_tool_calls": MaxToolCallsParam,
    },
)
~~~

The prompt parameter renders controls for editing the prompt and model.
`MaxToolCallsParam` exposes the runtime limit without exposing the rest of the agent
configuration.

Push from inside `evals`:

~~~bash
cd evals
bt functions push parameters.py --env-file ../.env
~~~

In Braintrust, confirm that the prompt, model, and maximum-tool-calls controls are visible in the **Parameters** tab.

## Step 2: Write the remote eval task

Open **evals/eval_agent_remote_server.py**. Add these imports below the path setup:

~~~python
import uuid

from braintrust import Eval, init_function, load_parameters

from agent.agent import Agent, InputFile
from agent.config import AgentConfig

PROJECT = "learn-bt"
saved_parameters = load_parameters(project=PROJECT, slug="sales-assistant-parameters")
~~~

Replace the commented-out task and eval template with:

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
    parameters=saved_parameters,
)
~~~

The task converts `hooks.parameters` from the playground into `AgentConfig`,
runs the agent, and returns its output. Preserve history and attachments so
follow-up requests retain their context.

Leave `data=[]` because you will select the dataset in the playground.
Scorers selected there run alongside those defined in the server.

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
eval source, and choose **crm-recipient-mismatches**. Keep the dataset and both
scorers unchanged throughout the following comparison.

## Step 4: Run the current configuration

Use the saved parameter defaults, which reflect the current application config.
Run the dataset and label this variant **Current configuration**. Inspect its
recipient and email-quality results. Compare them with the local experiment
for the current configuration; model and judge variation can cause some differences.

## Step 5: Compare an email-writing prompt variant

Duplicate the task in the playground and label the copy **Email quality
candidate**. Keep the model and tool-call limit the same so this experiment
changes only the system prompt.

Read the email-quality failures and their explanations, alongside the human
reviews recorded on the source traces. Add guidance to the candidate's system prompt that
addresses the recurring issue. For example:

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

## Step 6: Apply the chosen configuration

If the candidate improves the drafts without reducing recipient correctness,
copy its complete system prompt into `SYSTEM_PROMPT` in **agent/config.py**.
Otherwise, keep the current configuration and record the unresolved issue.
Playground parameter edits do not automatically update the application.

Set the local eval's experiment name to `email-quality-selected-config` and run:

~~~bash
bt eval evals/eval_agent.py --env-file .env
~~~

Verify that the application configuration produces the behavior you selected.
This dataset contains known recipient failures, so the results establish
performance on those cases.

## Answer key

Compare your completed source files with these answer keys:

- [`evals/parameters.py`](solutions/06-remote-eval-server/evals/parameters.py)
- [`evals/eval_agent_remote_server.py`](solutions/06-remote-eval-server/evals/eval_agent_remote_server.py)
