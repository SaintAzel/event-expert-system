import pytest
from fastapi.testclient import TestClient

from event_expert.app import create_app


@pytest.fixture()
def client():
    return TestClient(create_app())


@pytest.fixture()
def all_ready_facts():
    return {
        "F001", "F002", "F005",
        "F006", "F007", "F010",
        "F011", "F012", "F015",
        "F016", "F017", "F020",
        "F021", "F022", "F025",
        "F026", "F027", "F030",
        "F031", "F032", "F035",
        "F036", "F037", "F040",
    }
