"""
Recommendation Engine
=====================

Generate actionable recommendations from the
Forward Chaining inference result.

Workflow
--------
InferenceResult
        ↓
Identify Missing Criteria
        ↓
Lookup Recommendation
        ↓
RecommendationResult
"""

from __future__ import annotations

from .models import (
    RecommendationItem,
    RecommendationResult,
)

from ..knowledge.models import (
    Criteria,
    InferenceResult,
    KnowledgeBase,
    Recommendation,
)


class RecommendationEngine:
    """
    Generate recommendations for every
    missing criterion.

    This engine never performs inference.
    It only maps missing criteria into
    actionable recommendations.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self.knowledge = knowledge

        # ==========================================
        # Lookup Tables
        # ==========================================

        self._criteria_by_id = {
            criteria.id: criteria
            for criteria in knowledge.criteria.data
        }

        self._recommendations_by_criteria = {
            recommendation.criteria: recommendation
            for recommendation in knowledge.recommendations.data
        }

    # ==============================================
    # Public API
    # ==============================================

    def generate(
        self,
        inference: InferenceResult,
    ) -> RecommendationResult:
        """
        Generate recommendations from an
        InferenceResult.
        """

        matched_ids = {
            criteria.id
            for criteria in inference.matched_criteria
        }

        items: list[RecommendationItem] = []

        for criteria in self.knowledge.criteria.data:

            # Skip criteria yang sudah terpenuhi
            if criteria.id in matched_ids:
                continue

            recommendation = (
                self._recommendations_by_criteria.get(
                    criteria.id
                )
            )

            # Tidak ada recommendation
            if recommendation is None:
                continue

            items.append(
                self._build_item(
                    criteria,
                    recommendation,
                )
            )

        return RecommendationResult(
            items=items,
            total=len(items),
            inference=inference,
        )

    # ==============================================
    # Internal Helpers
    # ==============================================

    def _build_item(
        self,
        criteria: Criteria,
        recommendation: Recommendation,
    ) -> RecommendationItem:
        """
        Build one recommendation item.
        """

        return RecommendationItem(
            criteria=criteria,
            recommendation=recommendation,
            priority=criteria.priority,
        )