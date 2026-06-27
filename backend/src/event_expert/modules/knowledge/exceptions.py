"""
Knowledge Module Exceptions
===========================

Custom exception hierarchy used throughout the
Knowledge Module.

Every component should raise one of these exceptions
instead of using built-in RuntimeError or ValueError.
"""

from __future__ import annotations


class KnowledgeError(Exception):
    """
    Base exception for the Knowledge Module.
    """

    pass


# ==========================================================
# Repository Exceptions
# ==========================================================


class RepositoryError(KnowledgeError):
    """
    Base exception for repository-related errors.
    """

    pass


class RepositoryNotFoundError(RepositoryError):
    """
    Raised when the knowledge repository
    or one of its files cannot be found.
    """

    pass


class RepositoryValidationError(RepositoryError):
    """
    Raised when repository validation fails.
    """

    pass


class RepositoryLoadingError(RepositoryError):
    """
    Raised when repository loading fails.
    """

    pass


# ==========================================================
# Knowledge Base Exceptions
# ==========================================================


class KnowledgeBaseError(KnowledgeError):
    """
    Base exception related to the in-memory Knowledge Base.
    """

    pass


class KnowledgeBaseNotInitializedError(KnowledgeBaseError):
    """
    Raised when the Knowledge Base has not yet been loaded.
    """

    pass


# ==========================================================
# Inference Engine Exceptions
# ==========================================================


class InferenceEngineError(KnowledgeError):
    """
    Base exception for inference engine failures.
    """

    pass


class ForwardChainingError(InferenceEngineError):
    """
    Raised when an error occurs during
    Forward Chaining inference.
    """

    pass


class ExplanationEngineError(InferenceEngineError):
    """
    Raised when explanation generation fails.
    """

    pass


class RecommendationEngineError(InferenceEngineError):
    """
    Raised when recommendation generation fails.
    """

    pass