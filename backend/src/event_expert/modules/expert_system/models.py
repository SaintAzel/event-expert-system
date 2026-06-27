"""
Expert System Models
====================

Aggregate models produced by the
Expert System Service.
"""

from __future__ import annotations

from pydantic import Field

from ..evaluation.models import (
    EvaluationResult,
)

from ..explanation.models import (
    ExplanationResult,
)

from ..knowledge.models import (
    InferenceResult,
    KnowledgeBaseModel,
)

from ..recommendation.models import (
    RecommendationResult,
)


class ExpertSystemResult(KnowledgeBaseModel):
    """
    Aggregate result produced by the
    Expert System Service.
    """

    inference: InferenceResult

    explanation: ExplanationResult

    recommendation: RecommendationResult

    evaluation: EvaluationResult