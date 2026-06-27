"""
Forward Chaining Demonstration
==============================

Developer CLI for executing the complete
Forward Chaining pipeline.

Workflow
--------
Repository
    ↓
KnowledgeService
    ↓
KnowledgeBase
    ↓
ForwardChainingEngine
    ↓
InferenceResult
"""

from __future__ import annotations

import sys
from pathlib import Path

# ==========================================================
# Allow importing from src/
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

# ==========================================================
# Imports
# ==========================================================

from event_expert.modules.inference.forward_chaining import (
    ForwardChainingEngine,
)

from event_expert.modules.knowledge import (
    KnowledgeService,
)

# ==========================================================
# Demo Facts
# ==========================================================

SELECTED_FACTS = {
    # C01
    "F001",
    "F002",
    "F005",

    # C02
    "F006",
    "F007",
    "F010",

    # C03
    "F011",
    "F012",
    "F015",

    # C04
    "F016",
    "F017",
    "F020",

    # C05
    "F021",
    "F022",
    "F025",

    # C06
    "F026",
    "F027",
    "F030",

    # C07
    "F031",
    "F032",
    "F035",

    # C08
    "F036",
    "F037",
    "F040",
}

# ==========================================================
# Main
# ==========================================================


def main() -> None:

    print("=" * 60)
    print("EVENT EXPERT SYSTEM")
    print("Forward Chaining Demonstration")
    print("=" * 60)

    service = KnowledgeService()

    knowledge = service.get()

    engine = ForwardChainingEngine(
        knowledge
    )

    result = engine.infer(
        selected_facts=SELECTED_FACTS
    )

    print("\nSelected Facts")
    print("-" * 60)

    for fact in result.triggered_facts:
        print(f"✓ {fact.id} - {fact.name}")

    print("\nMatched Criteria")
    print("-" * 60)

    for criteria in result.matched_criteria:
        print(f"✓ {criteria.id} - {criteria.name}")

    print("\nMatched Rules")
    print("-" * 60)

    for rule in result.matched_rules:
        print(
            f"✓ {rule.id} ({rule.rule_type})"
        )

    print("\nDecision")
    print("-" * 60)

    print(result.decision.name)

    print("\nExecution Time")
    print("-" * 60)

    print(
        f"{result.execution_time_ms:.3f} ms"
    )

    print("\n" + "=" * 60)
    print("Inference Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()