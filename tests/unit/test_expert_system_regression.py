import pytest

from event_expert.modules.expert_system import ExpertSystemService
from event_expert.modules.knowledge import KnowledgeService


@pytest.fixture()
def expert_system():
    knowledge = KnowledgeService().get()
    return ExpertSystemService(knowledge)


@pytest.mark.unit
def test_forward_chaining_matches_all_eight_criteria_for_complete_facts(
    expert_system,
    all_ready_facts,
):
    result = expert_system.run(all_ready_facts)

    assert result.inference.decision.id == "D001"
    assert result.evaluation.matched_criteria == 8
    assert result.evaluation.missing_criteria == 0
    assert result.evaluation.completion_percentage == 100


@pytest.mark.unit
def test_forward_chaining_requires_all_conditions_in_a_category_rule(expert_system):
    incomplete_legal_facts = {"F001", "F002"}

    result = expert_system.run(incomplete_legal_facts)

    matched_criteria_ids = {criteria.id for criteria in result.inference.matched_criteria}

    assert "RC01" not in matched_criteria_ids
    assert result.inference.decision.id == "D003"
    assert result.evaluation.risk_level == "HIGH"


@pytest.mark.unit
def test_recommendations_are_generated_for_missing_criteria(expert_system):
    result = expert_system.run(set())

    recommendation_criteria_ids = {
        recommendation.criteria.id
        for recommendation in result.recommendation.items
    }

    assert result.inference.decision.id == "D003"
    assert "RC01" in recommendation_criteria_ids
    assert "RC08" in recommendation_criteria_ids
