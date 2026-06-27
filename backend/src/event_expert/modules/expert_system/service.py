"""
Expert System Service
=====================

Facade for executing the complete
Expert System pipeline.
"""

from __future__ import annotations

from .models import (
    ExpertSystemResult,
)

from ..evaluation.engine import (
    EvaluationEngine,
)

from ..explanation.engine import (
    ExplanationEngine,
)

from ..inference.forward_chaining import (
    ForwardChainingEngine,
)

from ..knowledge.models import (
    FactId,
    KnowledgeBase,
)

from ..recommendation.engine import (
    RecommendationEngine,
)


class ExpertSystemService:
    """
    High-level facade for the
    Event Expert System.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self.forward_chaining = (
            ForwardChainingEngine(
                knowledge
            )
        )

        self.explanation = (
            ExplanationEngine(
                knowledge
            )
        )

        self.recommendation = (
            RecommendationEngine(
                knowledge
            )
        )

        self.evaluation = (
            EvaluationEngine(
                knowledge
            )
        )

    # ==================================================
    # Public API
    # ==================================================

    def run(
        self,
        selected_facts: set[FactId],
    ) -> ExpertSystemResult:
        """
        Execute the complete expert system.
        """

        inference = (
            self.forward_chaining.infer(
                selected_facts
            )
        )

        explanation = (
            self.explanation.explain(
                inference
            )
        )

        recommendation = (
            self.recommendation.generate(
                inference
            )
        )

        evaluation = (
            self.evaluation.evaluate(
                inference
            )
        )

        return ExpertSystemResult(
            inference=inference,
            explanation=explanation,
            recommendation=recommendation,
            evaluation=evaluation,
        )