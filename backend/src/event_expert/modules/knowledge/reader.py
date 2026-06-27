"""
Knowledge Repository Reader

Responsible only for reading repository JSON files.

This module DOES NOT perform:
- validation
- inference
- business logic

It only returns raw dictionary objects.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FILES = {
    "metadata": ("metadata.json",),
    "categories": ("categories.json",),
    "facts": ("facts.json",),
    "criteria": ("criteria.json",),
    "decisions": ("decisions.json",),
    "recommendations": ("recommendations.json",),
    "category_rules": ("rules", "category_rules.json"),
    "global_rules": ("rules", "global_rules.json"),
}


class KnowledgeRepositoryReader:
    """
    Read every repository JSON file.

    This class is intentionally simple and only performs
    filesystem I/O.
    """

    def __init__(self, repository_path: Path):
        self.repository_path = repository_path

    def _read_json(self, *parts: str) -> dict[str, Any]:
        """
        Read a JSON file from the repository.

        Parameters
        ----------
        *parts:
            Relative path components.

        Returns
        -------
        dict
            Parsed JSON object.
        """

        path = self.repository_path.joinpath(*parts)

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def read_metadata(self) -> dict[str, Any]:
        return self._read_json(*FILES["metadata"])

    def read_categories(self) -> dict[str, Any]:
        return self._read_json(*FILES["categories"])

    def read_facts(self) -> dict[str, Any]:
        return self._read_json(*FILES["facts"])

    def read_criteria(self) -> dict[str, Any]:
        return self._read_json(*FILES["criteria"])

    def read_decisions(self) -> dict[str, Any]:
        return self._read_json(*FILES["decisions"])

    def read_recommendations(self) -> dict[str, Any]:
        return self._read_json(*FILES["recommendations"])

    def read_category_rules(self) -> dict[str, Any]:
        return self._read_json(*FILES["category_rules"])

    def read_global_rules(self) -> dict[str, Any]:
        return self._read_json(*FILES["global_rules"])