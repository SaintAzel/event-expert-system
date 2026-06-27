"""
Recommendation Engine Demonstration
==================================
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from event_expert.modules.inference.forward_chaining import (
    ForwardChainingEngine,
)

from event_expert.modules.knowledge import (
    KnowledgeService,
)

from event_expert.modules.recommendation.engine import (
    RecommendationEngine,
)

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


def main():

    print("=" * 60)
    print("RECOMMENDATION ENGINE DEMO")
    print("=" * 60)

    knowledge = KnowledgeService().get()

    inference = ForwardChainingEngine(
        knowledge
    ).infer(
        SELECTED_FACTS
    )

    recommendations = RecommendationEngine(
        knowledge
    ).generate(
        inference
    )

    print()

    print(
        f"Decision : {inference.decision.name}"
    )

    print(
        f"Recommendation : {recommendations.total}"
    )

    print("-" * 60)

    if recommendations.total == 0:

        print(
            "No recommendation required."
        )

    else:

        for item in recommendations.items:

            print(
                f"[{item.priority.upper()}]"
            )

            print(
                item.recommendation.title
            )

            print(
                item.recommendation.description
            )

            print()
            

if __name__ == "__main__":
    main()