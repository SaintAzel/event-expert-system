"""
Knowledge Exceptions
====================

Domain-specific exceptions for the
Event Expert System.

These exceptions are raised by the
Knowledge, Inference, Explanation,
Recommendation, Evaluation, and
Expert System modules.

This module MUST NOT depend on
FastAPI or any HTTP-related package.
"""

from __future__ import annotations


# ==========================================================
# Base Exception
# ==========================================================


class KnowledgeError(Exception):
    """
    Base exception for the Event Expert System.
    """


# ==========================================================
# Repository Exceptions
# ==========================================================


class RepositoryLoadingError(KnowledgeError):
    """
    Raised when a knowledge repository
    cannot be loaded.
    """


class RepositoryValidationError(KnowledgeError):
    """
    Raised when the repository contains
    invalid or inconsistent knowledge.
    """


class KnowledgeBaseNotInitializedError(KnowledgeError):
    """
    Raised when attempting to access the
    KnowledgeBase before it has been loaded.
    """


# ==========================================================
# Inference Exceptions
# ==========================================================


class ForwardChainingError(KnowledgeError):
    """
    Raised when no inference result
    can be produced.
    """


# ==========================================================
# Explanation Exceptions
# ==========================================================


class ExplanationError(KnowledgeError):
    """
    Raised when explanation generation fails.
    """


# ==========================================================
# Recommendation Exceptions
# ==========================================================


class RecommendationError(KnowledgeError):
    """
    Raised when recommendation generation fails.
    """


# ==========================================================
# Evaluation Exceptions
# ==========================================================


class EvaluationError(KnowledgeError):
    """
    Raised when evaluation generation fails.
    """


# ==========================================================
# Expert System Exceptions
# ==========================================================


class ExpertSystemError(KnowledgeError):
    """
    Raised when the complete expert system
    execution fails.
    """