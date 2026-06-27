from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from event_expert.modules.expert_system import (
    ExpertSystemService,
)
from event_expert.modules.expert_system.formatter import (
    ExpertSystemFormatter,
)
from event_expert.modules.knowledge import (
    KnowledgeService,
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

    knowledge = KnowledgeService().get()

    service = ExpertSystemService(
        knowledge
    )

    result = service.run(
        SELECTED_FACTS
    )

    print(
        ExpertSystemFormatter.to_text(
            result
        )
    )


if __name__ == "__main__":
    main()