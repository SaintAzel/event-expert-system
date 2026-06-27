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
    # Internal Helpers
    # ======================================================

    def _ensure_validated(self) -> None:
        """
        Ensure that the repository has already been validated
        and every required repository has been loaded.
        """

        required_repositories = {
            "metadata": self.validator.metadata,
            "categories": self.validator.categories,
            "facts": self.validator.facts,
            "criteria": self.validator.criteria,
            "decisions": self.validator.decisions,
            "recommendations": self.validator.recommendations,
            "category_rules": self.validator.category_rules,
            "global_rules": self.validator.global_rules,
        }

        for repository_name, repository in required_repositories.items():

            if repository is None:

                raise RepositoryLoadingError(
                    f"{repository_name.capitalize()} repository "
                    "has not been loaded. "
                    "Make sure validator.validate() is called "
                    "before loader.load()."
                )
    # ======================================================
    # Public API
    # ======================================================

    def load(self) -> KnowledgeBase:
        """
        Build and return a validated KnowledgeBase.
        """

        self._ensure_validated()

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