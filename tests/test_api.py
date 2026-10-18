
import pytest

from app import create_app
from extensions import db


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_orders(client):
    response = client.get("/api/orders")
    assert response.status_code == 200
    assert "orders" in response.json


def test_fail_endpoint(client):
    response = client.get("/api/fail")
    assert response.status_code == 500
    assert "error" in response.json


def test_logs_endpoint(client):
    # This request itself is logged by the monitoring hook.
    response = client.get("/api/health")
    assert response.status_code == 200

    response = client.get("/api/logs")
    assert response.status_code == 200
    assert "logs" in response.json
    assert isinstance(response.json["logs"], list)


def test_failed_request_is_logged(client):
    response = client.get("/api/fail")
    assert response.status_code == 500

    response = client.get("/api/logs?status_code=500")
    assert response.status_code == 200

    failed_logs = response.json["logs"]
    assert any(
        log["endpoint"] == "/api/fail"
        and log["status_code"] == 500
        for log in failed_logs
    )


def test_invalid_status_code_filter(client):
    response = client.get("/api/logs?status_code=99")
    assert response.status_code == 400


def test_invalid_method_filter(client):
    response = client.get("/api/logs?method=OPTIONS")
    assert response.status_code == 400
