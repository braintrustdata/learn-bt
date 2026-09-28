import braintrust
from pydantic import BaseModel

project = braintrust.projects.create(name="learn-bt")


class TraceParams(BaseModel):
    trace: dict


async def recipient_matches_crm(trace=None):
    # TODO: Compare the drafted recipient with the CRM primary-contact email.
    pass

# project.scorers.create(TODO)
