import pytest


@pytest.mark.api
def test_evaluation_ready_path_returns_ready_decision(client, all_ready_facts):
    response = client.post("/evaluation", json={"facts": sorted(all_ready_facts)})

    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Evaluation completed successfully."
    assert body["data"]["inference"]["decision"]["id"] == "D001"
    assert body["data"]["inference"]["decision"]["name"] == "READY"
    assert body["data"]["evaluation"]["risk_level"] == "LOW"
    assert body["data"]["evaluation"]["completion_percentage"] == 100


@pytest.mark.api
def test_evaluation_improvement_path_returns_improvement_decision(client):
    facts = [
        "F001", "F002", "F005",
        "F006", "F007", "F010",
        "F011", "F012", "F015",
        "F016", "F017", "F020",
        "F021", "F022", "F025",
        "F026", "F027", "F030",
        "F031", "F032", "F035",
    ]

    response = client.post("/evaluation", json={"facts": facts})

    body = response.json()

    assert response.status_code == 200
    assert body["data"]["inference"]["decision"]["id"] == "D002"
    assert body["data"]["inference"]["decision"]["name"] == "IMPROVEMENT"
    assert body["data"]["evaluation"]["matched_criteria"] == 7
    assert body["data"]["evaluation"]["missing_criteria"] == 1


@pytest.mark.api
def test_evaluation_not_ready_path_accepts_empty_fact_selection(client):
    response = client.post("/evaluation", json={"facts": []})

    body = response.json()

    assert response.status_code == 200
    assert body["data"]["inference"]["decision"]["id"] == "D003"
    assert body["data"]["inference"]["decision"]["name"] == "NOT_READY"
    assert body["data"]["evaluation"]["risk_level"] == "HIGH"
    assert body["data"]["evaluation"]["matched_criteria"] == 0


@pytest.mark.api
def test_evaluation_rejects_invalid_fact_identifier(client):
    response = client.post("/evaluation", json={"facts": ["INVALID_FACT"]})

    assert response.status_code == 422


@pytest.mark.api
def test_evaluation_rejects_missing_facts_payload(client):
    response = client.post("/evaluation", json={})

    assert response.status_code == 422
