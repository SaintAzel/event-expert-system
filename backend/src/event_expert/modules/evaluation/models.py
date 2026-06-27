"""
Evaluation Models
=================

Data models produced by the Evaluation Engine.

The Evaluation Engine calculates quantitative
metrics from the inference result.

Responsibilities
----------------
- Represent readiness metrics
- Represent risk level
- Represent evaluation result
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from ..knowledge.models import (
    InferenceResult,
    KnowledgeBaseModel,
)

# ==========================================================
# Common Types
# ==========================================================

RiskLevel = Literal[
    "LOW",
    "MEDIUM",
    "HIGH",
]

# ==========================================================
# Evaluation Result
# ==========================================================


class EvaluationResult(KnowledgeBaseModel):
    """
    Quantitative evaluation generated from
    an inference result.
    """

    completion_percentage: float = Field(
        ...,
        ge=0,
        le=100,
    )

    matched_criteria: int = Field(
        ...,
        ge=0,
    )

    missing_criteria: int = Field(
        ...,
        ge=0,
    )

    total_criteria: int = Field(
        ...,
        gt=0,
    )

    risk_level: RiskLevel

    inference: InferenceResult