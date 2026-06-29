import pytest


@pytest.mark.api
def test_root_endpoint_returns_api_identity(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Event Expert System API",
        "version": "1.0.0",
    }


@pytest.mark.api
def test_version_endpoint_returns_api_and_knowledge_version(client):
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "api_version": "1.0.0",
        "knowledge_version": "1.0.0",
    }


@pytest.mark.api
def test_health_endpoint_returns_ok_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "event-expert-system",
    }
