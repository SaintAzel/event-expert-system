"""
Knowledge Cache
===============

Store the validated KnowledgeBase in memory.

Responsibilities
----------------
- Store KnowledgeBase
- Provide KnowledgeBase
- Clear KnowledgeBase
- Report cache status
"""

from __future__ import annotations

from .exceptions import KnowledgeBaseNotInitializedError
from .models import KnowledgeBase


class KnowledgeCache:
    """
    In-memory cache for the KnowledgeBase.

    This class does not build or validate the repository.
    It only stores the KnowledgeBase instance.
    """

    def __init__(self) -> None:
        self._knowledge: KnowledgeBase | None = None

    # ======================================================
    # Public API
    # ======================================================

    def set(self, knowledge: KnowledgeBase) -> None:
        """
        Store a KnowledgeBase instance.
        """

        self._knowledge = knowledge

    def get(self) -> KnowledgeBase:
        """
        Return the cached KnowledgeBase.

        Raises
        ------
        KnowledgeBaseNotInitializedError
            If the cache has not been initialized.
        """

        if self._knowledge is None:
            raise KnowledgeBaseNotInitializedError(
                "KnowledgeBase has not been initialized."
            )

        return self._knowledge

    def clear(self) -> None:
        """
        Remove the cached KnowledgeBase.
        """

        self._knowledge = None

    def is_loaded(self) -> bool:
        """
        Return True if a KnowledgeBase
        has been cached.
        """

        return self._knowledge is not None