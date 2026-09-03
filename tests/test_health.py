from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_reports_ok_for_memory_backend():
    from src.app.state import MemoryState

    with patch("src.routes.health.get_state_instance", return_value=MemoryState()):
        response = client.get("/readiness/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"database": "not applicable (memory backend)"}}


def test_readiness_checks_db_connection_for_sqlite_backend():
    from src.app.state import SQLAlchemyState

    with patch("src.routes.health.get_state_instance", return_value=SQLAlchemyState()):
        response = client.get("/readiness/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"database": "ok"}}


def test_readiness_returns_503_when_the_database_is_unreachable():
    from sqlalchemy.exc import SQLAlchemyError

    from src.app.state import SQLAlchemyState

    with patch("src.routes.health.get_state_instance", return_value=SQLAlchemyState()):
        with patch("src.routes.health.engine.connect", side_effect=SQLAlchemyError("unable to open database file")):
            response = client.get("/readiness/")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "error"
    assert "unable to open database file" in body["checks"]["database"]
