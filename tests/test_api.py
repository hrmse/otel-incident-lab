import os

from fastapi.testclient import TestClient

os.environ["OTEL_EXPORT_ENABLED"] = "false"

from checkout_api.main import app

client = TestClient(app)


def test_healthcheck_is_available() -> None:
    assert client.get("/healthz").json() == {"status": "ok"}


def test_checkout_is_synthetic_success_by_default() -> None:
    response = client.get("/checkout/order-123")
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"


def test_debug_failure_is_disabled_without_explicit_lab_flag() -> None:
    response = client.get("/checkout/order-123", headers={"X-Debug-Fail": "true"})
    assert response.status_code == 200


def test_debug_failure_requires_header_and_explicit_lab_flag(monkeypatch) -> None:
    monkeypatch.setenv("LAB_ALLOW_DEBUG_FAILURES", "true")
    response = client.get("/checkout/order-123", headers={"X-Debug-Fail": "true"})
    assert response.status_code == 503
