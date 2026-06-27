"""
Knowledge Domain Models
=======================

This module defines all Pydantic models used by the
Event Expert System Knowledge Repository.

These models act as the single source of truth for:

- Knowledge Repository
- Repository Validator
- Knowledge Loader
- Forward Chaining Engine
- Explanation Engine
- Recommendation Engine
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

# ==========================================================
# Common Types
# ==========================================================

PriorityLevel = Literal[
    "critical",
    "high",
    "medium",
    "low",
]

# ==========================================================
# Typed ID Definitions
# ==========================================================

CategoryId = Annotated[
    str,
    Field(pattern=r"^C\d{2}$")
]

FactId = Annotated[
    str,
    Field(pattern=r"^F\d{3}$")
]

CriteriaId = Annotated[
    str,
    Field(pattern=r"^RC\d{2}$")
]

DecisionId = Annotated[
    str,
    Field(pattern=r"^D\d{3}$")
]

RecommendationId = Annotated[
    str,
    Field(pattern=r"^REC\d{3}$")
]

CategoryRuleId = Annotated[
    str,
    Field(pattern=r"^CR\d{3}$")
]

GlobalRuleId = Annotated[
    str,
    Field(pattern=r"^GR\d{3}$")
]

# ==========================================================
# Base Model
# ==========================================================


class KnowledgeBaseModel(BaseModel):
    """
    Base model for every knowledge object.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )


# ==========================================================
# Knowledge Models
# ==========================================================


class Category(KnowledgeBaseModel):
    """
    Knowledge Category.
    """

    id: CategoryId
    name: str = Field(..., min_length=1)
    priority: PriorityLevel


class Fact(KnowledgeBaseModel):
    """
    Knowledge Fact.
    """

    id: FactId

    category: CategoryId

    name: str = Field(..., min_length=1)

    description: str = Field(..., min_length=1)

    evidence: str = Field(..., min_length=1)

    critical: bool


class Criteria(KnowledgeBaseModel):
    """
    Criteria produced after category rule evaluation.
    """

    id: CriteriaId

    category: CategoryId

    name: str = Field(..., min_length=1)

    description: str = Field(..., min_length=1)

    priority: PriorityLevel


class Decision(KnowledgeBaseModel):
    """
    Final decision.
    """

    id: DecisionId

    name: str = Field(..., min_length=1)

    description: str = Field(..., min_length=1)


class Recommendation(KnowledgeBaseModel):
    """
    Recommendation generated from failed criteria.
    """

    id: RecommendationId

    criteria: CriteriaId

    title: str = Field(..., min_length=1)

    description: str = Field(..., min_length=1)


# ==========================================================
# Rule Models
# ==========================================================


class CategoryRule(KnowledgeBaseModel):
    """
    Rule used to infer category criteria.
    """

    id: CategoryRuleId

    priority: PriorityLevel

    conditions: list[FactId]

    conclusion: CriteriaId


class GlobalRule(KnowledgeBaseModel):
    """
    Rule used to infer final decision.
    """

    id: GlobalRuleId

    priority: int = Field(..., ge=1)

    conditions: list[CriteriaId]

    decision: DecisionId


# ==========================================================
# Metadata Models
# ==========================================================


class RepositoryStatistics(KnowledgeBaseModel):
    """
    Repository statistics.
    """

    categories: int

    facts: int

    criteria: int

    category_rules: int

    global_rules: int

    decisions: int

    recommendations: int


class KnowledgeMetadata(KnowledgeBaseModel):
    """
    Repository metadata.
    """

    knowledge_version: str

    method: str

    author: str

    last_updated: str

    statistics: RepositoryStatistics


# ==========================================================
# Repository Wrapper Models
# ==========================================================


class CategoryRepository(KnowledgeBaseModel):
    """
    Category Repository.
    """

    data: list[Category] = Field(default_factory=list)


class FactRepository(KnowledgeBaseModel):
    """
    Fact Repository.
    """

    data: list[Fact] = Field(default_factory=list)


class CriteriaRepository(KnowledgeBaseModel):
    """
    Criteria Repository.
    """

    data: list[Criteria] = Field(default_factory=list)


class DecisionRepository(KnowledgeBaseModel):
    """
    Decision Repository.
    """

    data: list[Decision] = Field(default_factory=list)


class RecommendationRepository(KnowledgeBaseModel):
    """
    Recommendation Repository.
    """

    data: list[Recommendation] = Field(default_factory=list)


class CategoryRuleRepository(KnowledgeBaseModel):
    """
    Category Rule Repository.
    """

    data: list[CategoryRule] = Field(default_factory=list)


class GlobalRuleRepository(KnowledgeBaseModel):
    """
    Global Rule Repository.
    """

    data: list[GlobalRule] = Field(default_factory=list)


# ==========================================================
# Aggregate Knowledge Base
# ==========================================================


class KnowledgeBase(KnowledgeBaseModel):
    """
    Complete Knowledge Base loaded into memory.

    This object will be consumed by:
    - Forward Chaining Engine
    - Explanation Engine
    - Recommendation Engine
    """

    metadata: KnowledgeMetadata

    categories: CategoryRepository

    facts: FactRepository

    criteria: CriteriaRepository

    decisions: DecisionRepository

    recommendations: RecommendationRepository

    category_rules: CategoryRuleRepository

    global_rules: GlobalRuleRepository
    

# ==========================================================
# Runtime Inference Models
# ==========================================================


class MatchedRule(KnowledgeBaseModel):
    """
    Rule that successfully matched during inference.
    """

    id: CategoryRuleId | GlobalRuleId = Field(
        ...,
        description="Rule identifier (CRxxx or GRxxx)."
    )

    rule_type: Literal[
        "category",
        "global",
    ]

    conditions: list[FactId | CriteriaId] = Field(
        default_factory=list,
        description="Conditions evaluated by this rule."
    )

    conclusion: CriteriaId | DecisionId = Field(
        ...,
        description="Criteria ID or Decision ID produced."
    )


class InferenceResult(KnowledgeBaseModel):
    """
    Final inference result produced by the
    Forward Chaining Engine.
    """
    decision: Decision
    
    matched_criteria: list[Criteria] = Field(
        default_factory=list
    )

    matched_rules: list[MatchedRule] = Field(
        default_factory=list
    )

    triggered_facts: list[Fact] = Field(
        default_factory=list
    )

    missing_criteria: list[Criteria] = Field(
        default_factory=list
    )

    execution_time_ms: float = Field(
        default=0.0,
        ge=0,
    )