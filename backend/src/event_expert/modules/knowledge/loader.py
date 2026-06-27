"""
Knowledge Loader
================

Build a validated KnowledgeBase object from the
Knowledge Repository.

Responsibilities
----------------
- Build KnowledgeBase
- Consume validated repositories
- Never read JSON directly
- Never perform validation
"""

from __future__ import annotations

from .exceptions import RepositoryLoadingError
from .models import KnowledgeBase
from .validator import KnowledgeRepositoryValidator


class KnowledgeLoader:
    """
    Build an in-memory KnowledgeBase.

    The loader assumes that the repository has already
    been validated successfully.
    """

    def __init__(
        self,
        validator: KnowledgeRepositoryValidator,
    ) -> None:

        self.validator = validator

    # ======================================================
    # Public API
    # ======================================================

    def load(self) -> KnowledgeBase:
        """
        Build and return a KnowledgeBase instance.

        Returns
        -------
        KnowledgeBase
            Fully populated knowledge base.
        """

        if self.validator.metadata is None:
            raise RepositoryLoadingError(
                "Repository has not been validated."
            )

        if self.validator.categories is None:
            raise RepositoryLoadingError(
                "Categories repository is unavailable."
            )

        if self.validator.facts is None:
            raise RepositoryLoadingError(
                "Facts repository is unavailable."
            )

        if self.validator.criteria is None:
            raise RepositoryLoadingError(
                "Criteria repository is unavailable."
            )

        if self.validator.decisions is None:
            raise RepositoryLoadingError(
                "Decisions repository is unavailable."
            )

        if self.validator.recommendations is None:
            raise RepositoryLoadingError(
                "Recommendations repository is unavailable."
            )

        if self.validator.category_rules is None:
            raise RepositoryLoadingError(
                "Category Rules repository is unavailable."
            )

        if self.validator.global_rules is None:
            raise RepositoryLoadingError(
                "Global Rules repository is unavailable."
            )

        return KnowledgeBase(
            metadata=self.validator.metadata,
            categories=self.validator.categories,
            facts=self.validator.facts,
            criteria=self.validator.criteria,
            decisions=self.validator.decisions,
            recommendations=self.validator.recommendations,
            category_rules=self.validator.category_rules,
            global_rules=self.validator.global_rules,
        )