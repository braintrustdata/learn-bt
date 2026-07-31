import os

import braintrust
from autoevals import LLMClassifier
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

project = braintrust.projects.create(name="learn-bt")  # Idempotent operation

# This example uses the Braintrust Gateway for LLM calls. This judge client is
# provided as reference to use as the client for the LLM Judge
judge_client = OpenAI(
    base_url=os.getenv("BRAINTRUST_AI_GATEWAY_URL") or "https://gateway.braintrust.dev",
    api_key=os.environ["BRAINTRUST_API_KEY"],
    default_headers={"x-bt-org-name": os.getenv("BRAINTRUST_ORG_NAME", "")},
)


# --- Code scorer -----------------------------------------------------------
class TraceParams(BaseModel):
    trace: dict


async def valid_email(trace=None):
    #TODO
    pass

# --- LLM-judge scorer ------------------------------------------------------
scorer_prompt = "TODO"

email_goal_reached_scorer = LLMClassifier(
    name="Email Goal Reached",
    prompt_template=scorer_prompt,
    choice_scores={"Y": 1, "N": 0},
    use_cot=True,
    client=judge_client,
)


class JudgeParams(BaseModel):
    input: dict
    trace: dict


async def email_goal_reached(input=None, trace=None):
    #TODO
    pass


# --- Register for push -----------------------------------------------------
#project.scorers.create(TODO)

#project.scorers.create(TODO)