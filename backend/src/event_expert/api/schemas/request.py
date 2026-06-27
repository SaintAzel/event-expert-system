from pydantic import BaseModel, Field

from ...modules.knowledge.models import FactId


class EvaluationRequest(BaseModel):
    """
    API request for event evaluation.
    """

    facts: set[FactId] = Field(
        ...,
        description="Selected fact identifiers.",
    )