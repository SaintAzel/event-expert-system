"""
Recommendation Models
=====================

Data models produced by the Recommendation Engine.

The Recommendation Engine transforms an
InferenceResult into actionable recommendations.

Responsibilities
----------------
- Represent recommendation items
- Represent recommendation result
"""

from __future__ import annotations

from pydantic import Field

from ..knowledge.models import (
    Criteria,
    InferenceResult,
    KnowledgeBaseModel,
    Recommendation,
    PriorityLevel,
)


# ==========================================================
# Recommendation Item
# ==========================================================


class RecommendationItem(KnowledgeBaseModel):
    """
    Recommendation for one missing criterion.
    """

    criteria: Criteria

    recommendation: Recommendation

    priority: PriorityLevel = Field(
        ...,
        min_length=1,
    )


# ==========================================================
# Recommendation Result
# ==========================================================


class RecommendationResult(KnowledgeBaseModel):

    items: list[RecommendationItem] = Field(
        default_factory=list
    )

    total: int = 0

    inference: InferenceResult