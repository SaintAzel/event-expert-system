"""
Evaluation API Router
=====================

REST API endpoint for evaluating
event readiness.
"""

from fastapi import APIRouter, Depends

from ..dependencies import (
    get_knowledge_service,
)

from ..schemas.request import (
    EvaluationRequest,
)

from ..schemas.response import (
    EvaluationResponse,
)

from ...modules.expert_system import (
    ExpertSystemService,
)

from ...modules.knowledge import (
    KnowledgeService,
)

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"],
)


@router.post(
    "",
    response_model=EvaluationResponse,
)
def evaluate(
    request: EvaluationRequest,
    knowledge_service: KnowledgeService = Depends(
        get_knowledge_service,
    ),
) -> EvaluationResponse:
    """
    Evaluate event readiness.
    """

    knowledge = knowledge_service.get()

    expert = ExpertSystemService(
        knowledge,
    )

    result = expert.run(
        request.facts,
    )

    return EvaluationResponse(
        data=result,
    )