"""
Knowledge Service
=================

Facade for building and providing the KnowledgeBase.

Responsibilities
----------------
- Read repository
- Validate repository
- Build KnowledgeBase
- Cache KnowledgeBase
"""

from __future__ import annotations

from pathlib import Path

from .cache import KnowledgeCache
from .loader import KnowledgeLoader
from .models import KnowledgeBase
from .reader import KnowledgeRepositoryReader
from .validator import KnowledgeRepositoryValidator


class KnowledgeService:
    """
    Facade for the Knowledge Layer.

    This class orchestrates:

    Repository
        ↓
    Reader
        ↓
    Validator
        ↓
    Loader
        ↓
    Cache
    """

    def __init__(self) -> None:

        repository_path = (
            Path(__file__)
            .parent
            .joinpath("repository")
        )

        self.reader = KnowledgeRepositoryReader(
            repository_path
        )

        self.validator = KnowledgeRepositoryValidator(
            self.reader
        )

        self.loader = KnowledgeLoader(
            self.validator
        )

        self.cache = KnowledgeCache()

    # ==================================================
    # Public API
    # ==================================================

    def load(self) -> KnowledgeBase:
        """
        Build and cache the KnowledgeBase.

        Returns
        -------
        KnowledgeBase
        """

        if self.cache.is_loaded():
            return self.cache.get()

        self.validator.validate()

        knowledge = self.loader.load()

        self.cache.set(knowledge)

        return knowledge

    def get(self) -> KnowledgeBase:
        """
        Return cached KnowledgeBase.

        Automatically loads it on first access.
        """

        if not self.cache.is_loaded():
            return self.load()

        return self.cache.get()

    def reload(self) -> KnowledgeBase:
        """
        Reload repository from disk.
        """

        self.cache.clear()

        return self.load()

    def clear(self) -> None:
        """
        Clear cached KnowledgeBase.
        """

        self.cache.clear()