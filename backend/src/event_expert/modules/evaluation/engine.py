"""
Evaluation Engine
=================

Generate quantitative evaluation metrics from an
InferenceResult.

Workflow
--------
InferenceResult
        ↓
Calculate completion
        ↓
Determine risk level
        ↓
EvaluationResult
"""

from __future__ import annotations

from .models import (
    EvaluationResult,
    RiskLevel,
)

from ..knowledge.models import (
    InferenceResult,
    KnowledgeBase,
)


class EvaluationEngine:
    """
    Calculate quantitative readiness metrics.

    This engine never performs inference.

    It only evaluates the inference result.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self.knowledge = knowledge

        self._total_criteria = len(
            knowledge.criteria.data
        )

    # ======================================================
    # Public API
    # ======================================================

    def evaluate(
        self,
        inference: InferenceResult,
    ) -> EvaluationResult:
        """
        Evaluate an inference result.
        """

        matched = len(
            inference.matched_criteria
        )

        total = self._total_criteria

        missing = total - matched

        completion = (
            matched / total
        ) * 100

        return EvaluationResult(
            completion_percentage=completion,
            matched_criteria=matched,
            missing_criteria=missing,
            total_criteria=total,
            risk_level=self._risk_level(
                completion
            ),
            inference=inference,
        )

    # ======================================================
    # Internal Helpers
    # ======================================================

    def _risk_level(
        self,
        completion: float,
    ) -> RiskLevel:
        """
        Determine risk level based on
        completion percentage.
        """

        if completion >= 90:
            return "LOW"

        if completion >= 70:
            return "MEDIUM"

        return "HIGH"