import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret")

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_new_routes_require_bearer_authentication():
    for path in ("/api/v1/goals", "/api/v1/dashboard/summary", "/api/v1/export/transactions"):
        assert client.get(path).status_code == 401
