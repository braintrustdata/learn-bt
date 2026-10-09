import braintrust
from pydantic import BaseModel

project = braintrust.projects.create(name="learn-bt")


class TraceParams(BaseModel):
    trace: dict


async def recipient_matches_crm(trace=None):
    # TODO: Compare the drafted recipient with the CRM primary-contact email.
    pass


async def email_quality(trace):
    # TODO: Extract the drafted email and grade its communication style
    pass

# project.scorers.create(TODO)

# project.scorers.create(TODO)