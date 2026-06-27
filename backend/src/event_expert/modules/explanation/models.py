"""
Explanation Models
==================

Data models produced by the Explanation Engine.

The Explanation Engine transforms an InferenceResult
into a human-readable explanation without changing
the inference outcome.

Responsibilities
----------------
- Represent explanation data
- Represent category evaluation
- Represent final explanation result
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from ..knowledge.models import (
    Criteria,
    Decision,
    InferenceResult,
    KnowledgeBaseModel,
    MatchedRule,
)

# ==========================================================
# Common Types
# ==========================================================

ExplanationStatus = Literal[
    "matched",
    "missing",
]

# ==========================================================
# Explanation Item
# ==========================================================


class ExplanationItem(KnowledgeBaseModel):
    """
    Explanation for one evaluation criterion.
    """

    criteria: Criteria

    status: ExplanationStatus

    message: str = Field(
        ...,
        min_length=1,
    )


# ==========================================================
# Explanation Summary
# ==========================================================


class ExplanationSummary(KnowledgeBaseModel):
    """
    Overall explanation summary.
    """

    title: str

    description: str


# ==========================================================
# Final Explanation Result
# ==========================================================


class ExplanationResult(KnowledgeBaseModel):
    """
    Human-readable explanation produced from an
    InferenceResult.
    """

    decision: Decision

    summary: ExplanationSummary

    matched_items: list[ExplanationItem] = Field(
        default_factory=list
    )

    missing_items: list[ExplanationItem] = Field(
        default_factory=list
    )

    matched_rules: list[MatchedRule] = Field(
        default_factory=list
    )

    inference: InferenceResult