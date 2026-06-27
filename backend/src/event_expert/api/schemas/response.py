from pydantic import BaseModel, Field

from ...modules.expert_system.models import (
    ExpertSystemResult,
)


class EvaluationResponse(BaseModel):
    """
    API response for event evaluation.
    """

    success: bool = Field(
        default=True,
    )

    message: str = Field(
        default="Evaluation completed successfully.",
    )

    data: ExpertSystemResult