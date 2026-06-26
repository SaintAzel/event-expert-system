from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]

BACKEND_ROOT = PROJECT_ROOT / "backend"

SRC_DIR = BACKEND_ROOT / "src"

MODULE_DIR = SRC_DIR / "event_expert" / "modules"

KNOWLEDGE_DIR = MODULE_DIR / "knowledge"

REPOSITORY_DIR = KNOWLEDGE_DIR / "repository"

TEST_DIR = BACKEND_ROOT / "tests"