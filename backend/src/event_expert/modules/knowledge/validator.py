"""
Knowledge Repository Validator
==============================

Validate every Knowledge Repository before it is loaded
into the Expert System.

Responsibilities
----------------
- Load repository through KnowledgeRepositoryReader
- Validate repository structure
- Validate cross references
- Validate repository statistics
- Produce validation result

This module DOES NOT perform:
- JSON reading
- Inference
- Recommendation
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .exceptions import RepositoryValidationError
from .models import (
    CategoryRepository,
    CategoryRuleRepository,
    CriteriaRepository,
    DecisionRepository,
    FactRepository,
    GlobalRuleRepository,
    KnowledgeMetadata,
    RecommendationRepository,
)
from .reader import KnowledgeRepositoryReader


# ==========================================================
# Validation Result
# ==========================================================


@dataclass(slots=True)
class ValidationResult:
    """
    Result returned after repository validation.
    """

    success: bool = True

    errors: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)


# ==========================================================
# Repository Validator
# ==========================================================


class KnowledgeRepositoryValidator:
    """
    Validate every Knowledge Repository.

    Workflow

    Repository Reader
            ↓
    Pydantic Validation
            ↓
    Cross Reference Validation
            ↓
    Statistics Validation
            ↓
    Validation Result
    """

    def __init__(
        self,
        reader: KnowledgeRepositoryReader,
    ) -> None:

        self.reader = reader

        self.result = ValidationResult()

        self.metadata: KnowledgeMetadata | None = None

        self.categories: CategoryRepository | None = None

        self.facts: FactRepository | None = None

        self.criteria: CriteriaRepository | None = None

        self.decisions: DecisionRepository | None = None

        self.recommendations: RecommendationRepository | None = None

        self.category_rules: CategoryRuleRepository | None = None

        self.global_rules: GlobalRuleRepository | None = None
    
    # ======================================================
    # Internal Helpers
    # ======================================================

    def _add_error(
        self,
        message: str,
    ) -> None:
        """
        Add validation error.
        """

        self.result.errors.append(message)

    def _add_warning(
        self,
        message: str,
    ) -> None:
        """
        Add validation warning.
        """

        self.result.warnings.append(message)

    # ======================================================
    # Repository Loading
    # ======================================================

    def _load_repositories(self) -> None:
        """
        Load every repository into memory using
        KnowledgeRepositoryReader.
        """

        try:

            self.metadata = KnowledgeMetadata.model_validate(
                self.reader.read_metadata()
            )

            self.categories = CategoryRepository.model_validate(
                self.reader.read_categories()
            )

            self.facts = FactRepository.model_validate(
                self.reader.read_facts()
            )

            self.criteria = CriteriaRepository.model_validate(
                self.reader.read_criteria()
            )

            self.decisions = DecisionRepository.model_validate(
                self.reader.read_decisions()
            )

            self.recommendations = RecommendationRepository.model_validate(
                self.reader.read_recommendations()
            )

            self.category_rules = CategoryRuleRepository.model_validate(
                self.reader.read_category_rules()
            )

            self.global_rules = GlobalRuleRepository.model_validate(
                self.reader.read_global_rules()
            )

        except Exception as exc:

            raise RepositoryValidationError(
                f"Unable to load repository: {exc}"
            ) from exc
    
    # ======================================================
    # Duplicate ID Validation
    # ======================================================

    def _validate_duplicate_ids(self) -> None:
        """
        Validate duplicate IDs across every repository.
        """

        repositories = [
            ("Category", self.categories.data),
            ("Fact", self.facts.data),
            ("Criteria", self.criteria.data),
            ("Decision", self.decisions.data),
            ("Recommendation", self.recommendations.data),
            ("Category Rule", self.category_rules.data),
            ("Global Rule", self.global_rules.data),
        ]

        for repository_name, objects in repositories:

            ids = [obj.id for obj in objects]

            duplicates = {
                item
                for item in ids
                if ids.count(item) > 1
            }

            for duplicate in duplicates:

                self._add_error(
                    f"Duplicate {repository_name} ID: {duplicate}"
                )

    # ======================================================
    # Category Reference Validation
    # ======================================================

    def _validate_category_reference(self) -> None:
        """
        Validate every repository referencing Category.
        """

        category_ids = {
            category.id
            for category in self.categories.data
        }

        for fact in self.facts.data:

            if fact.category not in category_ids:

                self._add_error(
                    f"{fact.id} references unknown category '{fact.category}'."
                )

        for criteria in self.criteria.data:

            if criteria.category not in category_ids:

                self._add_error(
                    f"{criteria.id} references unknown category '{criteria.category}'."
                )

    # ======================================================
    # Recommendation Validation
    # ======================================================

    def _validate_recommendation_reference(self) -> None:
        """
        Validate Recommendation → Criteria reference.
        """

        criteria_ids = {
            criteria.id
            for criteria in self.criteria.data
        }

        for recommendation in self.recommendations.data:

            if recommendation.criteria not in criteria_ids:

                self._add_error(
                    f"{recommendation.id} references unknown criteria "
                    f"'{recommendation.criteria}'."
                )

    # ======================================================
    # Category Rule Validation
    # ======================================================

    def _validate_category_rules(self) -> None:
        """
        Validate Category Rule references.
        """

        fact_ids = {
            fact.id
            for fact in self.facts.data
        }

        criteria_ids = {
            criteria.id
            for criteria in self.criteria.data
        }

        for rule in self.category_rules.data:

            for condition in rule.conditions:

                if condition not in fact_ids:

                    self._add_error(
                        f"{rule.id} references unknown fact '{condition}'."
                    )

            if rule.conclusion not in criteria_ids:

                self._add_error(
                    f"{rule.id} references unknown criteria "
                    f"'{rule.conclusion}'."
                )

    # ======================================================
    # Global Rule Validation
    # ======================================================

    def _validate_global_rules(self) -> None:
        """
        Validate Global Rule references.
        """

        criteria_ids = {
            criteria.id
            for criteria in self.criteria.data
        }

        decision_ids = {
            decision.id
            for decision in self.decisions.data
        }

        for rule in self.global_rules.data:

            for condition in rule.conditions:

                if condition not in criteria_ids:

                    self._add_error(
                        f"{rule.id} references unknown criteria '{condition}'."
                    )

            if rule.decision not in decision_ids:

                self._add_error(
                    f"{rule.id} references unknown decision "
                    f"'{rule.decision}'."
                )
    # ======================================================
    # Metadata Statistics Validation
    # ======================================================

    def _validate_statistics(self) -> None:
        """
        Validate repository statistics declared
        in metadata.json.
        """

        statistics = self.metadata.statistics

        expected = {
            "categories": len(self.categories.data),
            "facts": len(self.facts.data),
            "criteria": len(self.criteria.data),
            "category_rules": len(self.category_rules.data),
            "global_rules": len(self.global_rules.data),
            "decisions": len(self.decisions.data),
            "recommendations": len(self.recommendations.data),
        }

        for key, actual in expected.items():

            declared = getattr(statistics, key)

            if declared != actual:

                self._add_error(
                    f"Metadata statistics mismatch for "
                    f"'{key}' "
                    f"(expected={actual}, metadata={declared})"
                )

    # ======================================================
    # Repository Coverage Validation
    # ======================================================

    def _validate_coverage(self) -> None:
        """
        Validate repository coverage.

        Coverage validation only produces warnings.
        """

        used_facts = set()

        for rule in self.category_rules.data:
            used_facts.update(rule.conditions)

        for fact in self.facts.data:

            if fact.id not in used_facts:

                self._add_warning(
                    f"{fact.id} is never used by any Category Rule."
                )

        used_criteria = set()

        for rule in self.global_rules.data:
            used_criteria.update(rule.conditions)

        for criteria in self.criteria.data:

            if criteria.id not in used_criteria:

                self._add_warning(
                    f"{criteria.id} is never used by any Global Rule."
                )

        recommendation_criteria = {
            recommendation.criteria
            for recommendation in self.recommendations.data
        }

        for criteria in self.criteria.data:

            if criteria.id not in recommendation_criteria:

                self._add_warning(
                    f"{criteria.id} has no recommendation."
                )

    # ======================================================
    # Public API
    # ======================================================

    def validate(self) -> ValidationResult:
        """
        Validate the entire Knowledge Repository.
        Returns
        -------
        ValidationResult
            Validation result containing success status,
            errors, and warnings.
        """

        # Reset validation result
        self.result = ValidationResult()

        # Load Repository
        self._load_repositories()
        
        assert self.metadata is not None

        assert self.categories is not None

        assert self.facts is not None

        assert self.criteria is not None

        assert self.decisions is not None

        assert self.recommendations is not None

        assert self.category_rules is not None

        assert self.global_rules is not None

        self._validate_duplicate_ids()

        self._validate_category_reference()

        self._validate_recommendation_reference()

        self._validate_category_rules()

        self._validate_global_rules()

        self._validate_statistics()

        self._validate_coverage()

        self.result.success = len(self.result.errors) == 0

        return self.result