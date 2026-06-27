"""
Expert System Formatter
=======================

Utilities for formatting the complete
Expert System result into human-readable output.

Supported Formats
-----------------
- Plain Text (CLI)
- Markdown
"""

from __future__ import annotations

from .models import ExpertSystemResult


class ExpertSystemFormatter:
    """
    Format an ExpertSystemResult into
    human-readable output.
    """

    # ======================================================
    # Plain Text
    # ======================================================

    @staticmethod
    def to_text(
        result: ExpertSystemResult,
    ) -> str:
        """
        Format result into plain text.
        """

        lines: list[str] = []

        lines.append("=" * 60)
        lines.append("EVENT EXPERT SYSTEM REPORT")
        lines.append("=" * 60)

        # --------------------------------------------------
        # Decision
        # --------------------------------------------------

        lines.append("")
        lines.append("Decision")
        lines.append("-" * 60)
        lines.append(result.inference.decision.name)

        # --------------------------------------------------
        # Evaluation
        # --------------------------------------------------

        evaluation = result.evaluation

        lines.append("")
        lines.append("Evaluation")
        lines.append("-" * 60)
        lines.append(
            f"Completion : {evaluation.completion_percentage:.2f}%"
        )
        lines.append(
            f"Risk Level : {evaluation.risk_level}"
        )
        lines.append(
            f"Matched Criteria : {evaluation.matched_criteria}"
        )
        lines.append(
            f"Missing Criteria : {evaluation.missing_criteria}"
        )

        # --------------------------------------------------
        # Matched Criteria
        # --------------------------------------------------

        lines.append("")
        lines.append("Matched Criteria")
        lines.append("-" * 60)

        for item in result.explanation.matched_items:

            lines.append(
                f"✓ {item.criteria.id} - {item.criteria.name}"
            )

        # --------------------------------------------------
        # Missing Criteria
        # --------------------------------------------------

        lines.append("")
        lines.append("Missing Criteria")
        lines.append("-" * 60)

        if not result.explanation.missing_items:

            lines.append("None")

        else:

            for item in result.explanation.missing_items:

                lines.append(
                    f"✗ {item.criteria.id} - {item.criteria.name}"
                )

        # --------------------------------------------------
        # Recommendations
        # --------------------------------------------------

        lines.append("")
        lines.append("Recommendations")
        lines.append("-" * 60)

        if not result.recommendation.items:

            lines.append(
                "No recommendation required."
            )

        else:

            for item in result.recommendation.items:

                lines.append(
                    f"[{item.priority.upper()}]"
                )

                lines.append(
                    item.recommendation.title
                )

                lines.append(
                    item.recommendation.description
                )

                lines.append("")

        # --------------------------------------------------
        # Rules
        # --------------------------------------------------

        lines.append("")
        lines.append("Matched Rules")
        lines.append("-" * 60)

        for rule in result.inference.matched_rules:

            lines.append(
                f"{rule.id} ({rule.rule_type})"
            )

        # --------------------------------------------------
        # Execution
        # --------------------------------------------------

        lines.append("")
        lines.append("Execution")
        lines.append("-" * 60)

        lines.append(
            f"{result.inference.execution_time_ms:.3f} ms"
        )

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    # ======================================================
    # Markdown
    # ======================================================

    @staticmethod
    def to_markdown(
        result: ExpertSystemResult,
    ) -> str:
        """
        Format result into Markdown.
        """

        md: list[str] = []

        md.append("# Event Expert System Report")

        md.append("")
        md.append("## Decision")
        md.append(result.inference.decision.name)

        md.append("")
        md.append("## Evaluation")

        evaluation = result.evaluation

        md.append(
            f"- Completion: **{evaluation.completion_percentage:.2f}%**"
        )
        md.append(
            f"- Risk Level: **{evaluation.risk_level}**"
        )
        md.append(
            f"- Matched Criteria: **{evaluation.matched_criteria}**"
        )
        md.append(
            f"- Missing Criteria: **{evaluation.missing_criteria}**"
        )

        md.append("")
        md.append("## Recommendations")

        if not result.recommendation.items:

            md.append(
                "- No recommendation required."
            )

        else:

            for item in result.recommendation.items:

                md.append(
                    f"- **{item.recommendation.title}**"
                )

                md.append(
                    f"  - {item.recommendation.description}"
                )

        return "\n".join(md)