"""
Explanation Engine Demonstration
===============================

Developer CLI for executing the
Explanation Engine.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from event_expert.modules.explanation.engine import (
    ExplanationEngine,
)

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

    "F001","F002","F005",

    "F006","F007","F010",

    "F011","F012","F015",

    "F016","F017","F020",

    "F021","F022","F025",

    "F026","F027","F030",

    "F031","F032","F035",

    "F036","F037","F040",
}


def main() -> None:

    print("=" * 60)
    print("EXPLANATION ENGINE DEMO")
    print("=" * 60)

    knowledge = KnowledgeService().get()

    inference = ForwardChainingEngine(
        knowledge
    ).infer(
        selected_facts=SELECTED_FACTS
    )

    explanation = ExplanationEngine(
        knowledge
    ).explain(
        inference
    )

    print("\nDecision")
    print("-" * 60)

    print(explanation.decision.name)

    print("\nSummary")
    print("-" * 60)

    print(explanation.summary.title)
    print(explanation.summary.description)

    print("\nMatched")
    print("-" * 60)

    for item in explanation.matched_items:

        print(
            f"✓ {item.criteria.name}"
        )

    print("\nMissing")
    print("-" * 60)

    if not explanation.missing_items:

        print("None")

    else:

        for item in explanation.missing_items:

            print(
                f"✗ {item.criteria.name}"
            )


if __name__ == "__main__":
    main()