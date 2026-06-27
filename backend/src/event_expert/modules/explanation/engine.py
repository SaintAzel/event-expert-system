"""
Explanation Engine
==================

Generate a human-readable explanation from the
Forward Chaining inference result.

Workflow
--------
InferenceResult
        ↓
Evaluate matched criteria
        ↓
Evaluate missing criteria
        ↓
Generate summary
        ↓
ExplanationResult
"""

from __future__ import annotations

from .models import (
    ExplanationItem,
    ExplanationResult,
    ExplanationSummary,
)

from ..knowledge.models import (
    Criteria,
    InferenceResult,
    KnowledgeBase,
)


class ExplanationEngine:
    """
    Generate explanation from an InferenceResult.

    This engine never performs inference.

    It only explains the inference result.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self.knowledge = knowledge

        self._criteria_by_id = {
            criteria.id: criteria
            for criteria in knowledge.criteria.data
        }

    # ======================================================
    # Public API
    # ======================================================

    def explain(
        self,
        inference: InferenceResult,
    ) -> ExplanationResult:
        """
        Generate explanation.
        """

        matched_ids = {
            criteria.id
            for criteria in inference.matched_criteria
        }

        matched_items: list[ExplanationItem] = []

        missing_items: list[ExplanationItem] = []

        for criteria in self.knowledge.criteria.data:

            if criteria.id in matched_ids:

                matched_items.append(
                    self._matched_item(criteria)
                )

            else:

                missing_items.append(
                    self._missing_item(criteria)
                )

        summary = self._build_summary(
            inference
        )

        return ExplanationResult(
            decision=inference.decision,
            summary=summary,
            matched_items=matched_items,
            missing_items=missing_items,
            matched_rules=inference.matched_rules,
            inference=inference,
        )

    # ======================================================
    # Internal Helpers
    # ======================================================

    def _matched_item(
        self,
        criteria: Criteria,
    ) -> ExplanationItem:
        """
        Build explanation for a matched criterion.
        """

        return ExplanationItem(
            criteria=criteria,
            status="matched",
            message=(
                f"{criteria.name} telah memenuhi "
                "persyaratan."
            ),
        )

    def _missing_item(
        self,
        criteria: Criteria,
    ) -> ExplanationItem:
        """
        Build explanation for a missing criterion.
        """

        return ExplanationItem(
            criteria=criteria,
            status="missing",
            message=(
                f"{criteria.name} belum memenuhi "
                "persyaratan."
            ),
        )

    def _build_summary(
        self,
        inference: InferenceResult,
    ) -> ExplanationSummary:
        """
        Generate overall explanation summary.
        """

        decision = inference.decision.name

        summaries = {
            "READY": (
                "Event Siap",
                (
                    "Seluruh kategori kesiapan telah "
                    "memenuhi persyaratan sehingga "
                    "event dinyatakan siap "
                    "diselenggarakan."
                ),
            ),
            "IMPROVEMENT": (
                "Perlu Peningkatan",
                (
                    "Sebagian besar kategori telah "
                    "memenuhi persyaratan, namun "
                    "masih terdapat aspek yang perlu "
                    "ditingkatkan."
                ),
            ),
            "NOT_READY": (
                "Belum Siap",
                (
                    "Kategori utama belum memenuhi "
                    "persyaratan sehingga event "
                    "belum layak diselenggarakan."
                ),
            ),
        }

        title, description = summaries.get(
            decision,
            (
                "Unknown",
                "No explanation available.",
            ),
        )

        return ExplanationSummary(
            title=title,
            description=description,
        )