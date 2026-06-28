"""
Forward Chaining Engine
=======================

Implementation of the Forward Chaining inference method
for the Event Expert System.

Workflow
--------
Selected Facts
        ↓
Category Rule Matching
        ↓
Matched Criteria
        ↓
Global Rule Matching
        ↓
Decision
        ↓
InferenceResult
"""

from __future__ import annotations

from time import perf_counter

from ..knowledge.exceptions import ForwardChainingError
from ..knowledge.models import (
    CategoryRule,
    Criteria,
    CriteriaId,
    Decision,
    Fact,
    FactId,
    GlobalRule,
    InferenceResult,
    KnowledgeBase,
    MatchedRule,
)
from collections.abc import Collection


class ForwardChainingEngine:
    """
    Forward Chaining inference engine.

    This engine performs two-stage inference:

    Facts
        ↓
    Criteria
        ↓
    Decision
    """

    def __init__(
    self,
    knowledge: KnowledgeBase,
    ) -> None:

        self.knowledge = knowledge

        # ==================================================
        # Lookup Tables
        # ==================================================

        self._facts_by_id = {
            fact.id: fact
            for fact in knowledge.facts.data
        }

        self._criteria_by_id = {
            criteria.id: criteria
            for criteria in knowledge.criteria.data
        }

        self._decisions_by_id = {
            decision.id: decision
            for decision in knowledge.decisions.data
        }

        # ==================================================
        # Rule Collections
        # ==================================================

        self._category_rules = knowledge.category_rules.data

        self._global_rules = knowledge.global_rules.data

        # ==================================================
        # Runtime State
        # ==================================================

        self._matched_category_rules: list[MatchedRule] = []

        self._matched_global_rules: list[MatchedRule] = []

    # ======================================================
    # Public API
    # ======================================================

    def infer(
        self,
        selected_facts: set[FactId],
    ) -> InferenceResult:
        """
        Execute Forward Chaining inference.

        Parameters
        ----------
        selected_facts:
            Selected fact identifiers.

        Returns
        -------
        InferenceResult
        """
        self._matched_category_rules.clear()
        self._matched_global_rules.clear()

        start_time = perf_counter()

        matched_criteria = self._match_category_rules(
            selected_facts
        )

        decision = self._match_global_rules(
            matched_criteria
        )

        execution_time = (
            perf_counter() - start_time
        ) * 1000

        return self._build_result(
            selected_facts=selected_facts,
            matched_criteria=matched_criteria,
            decision=decision,
            execution_time_ms=execution_time,
        )

    # ======================================================
    # Category Rule Matching
    # ======================================================

    def _match_category_rules(
        self,
        selected_facts: set[FactId],
    ) -> list[Criteria]:
        """
        Evaluate Category Rules and produce matched criteria.
        """

        matched_criteria: list[Criteria] = []

        matched_criteria_ids: set[CriteriaId] = set()

        for rule in self._category_rules:

            if not self._all_conditions_met(
                rule.conditions,
                selected_facts,
            ):
                continue

            if rule.conclusion in matched_criteria_ids:
                continue

            criteria = self._criteria_by_id[rule.conclusion]

            matched_criteria.append(criteria)

            matched_criteria_ids.add(criteria.id)

            self._matched_category_rules.append(
                MatchedRule(
                    id=rule.id,
                    rule_type="category",
                    conditions=list(rule.conditions),
                    conclusion=rule.conclusion,
                )
            )

        return matched_criteria

    # ======================================================
    # Global Rule Matching
    # ======================================================

    def _match_global_rules(
        self,
        matched_criteria: list[Criteria],
    ) -> Decision:
        """
        Evaluate Global Rules and produce the final decision.
        """

        matched_criteria_ids = {
            criteria.id
            for criteria in matched_criteria
        }

        for rule in sorted(
            self._global_rules,
            key=lambda rule: rule.priority,
        ):

            if not self._all_conditions_met(
                rule.conditions,
                matched_criteria_ids,
            ):
                continue

            decision = self._decisions_by_id[
                rule.decision
            ]

            self._matched_global_rules.append(
                MatchedRule(
                    id=rule.id,
                    rule_type="global",
                    conditions=list(rule.conditions),
                    conclusion=rule.decision,
                )
            )

            return decision

        return self._decisions_by_id[
            "D003"
        ]

    # ======================================================
    # Result Builder
    # ======================================================

    def _build_result(
        self,
        *,
        selected_facts: set[FactId],
        matched_criteria: list[Criteria],
        decision: Decision,
        execution_time_ms: float,
    ) -> InferenceResult:
        """
        Build InferenceResult.
        """
        
        triggered_facts = [
            self._facts_by_id[fact_id]
            for fact_id in sorted(selected_facts)
        ]

        matched_rules = (
            self._matched_category_rules
            + self._matched_global_rules
        )

        missing_criteria = self._collect_missing_criteria(
            matched_criteria
        )

        return InferenceResult(
            decision=decision,
            matched_criteria=matched_criteria,
            matched_rules=matched_rules,
            triggered_facts=triggered_facts,
            missing_criteria=missing_criteria,
            execution_time_ms=execution_time_ms,
        )
    
    # ======================================================
    # Internal Helpers
    # ======================================================

    def _collect_missing_criteria(
        self,
        matched_criteria: list[Criteria],
    ) -> list[Criteria]:
        """
        Return every criteria that was not inferred.
        """

        matched_ids = {
            criteria.id
            for criteria in matched_criteria
        }

        return [
            criteria
            for criteria in self.knowledge.criteria.data
            if criteria.id not in matched_ids
        ]

    def _all_conditions_met(
        self,
        conditions: Collection[FactId | CriteriaId],
        available: Collection[FactId | CriteriaId],
    ) -> bool:
        return all(condition in available for condition in conditions)
