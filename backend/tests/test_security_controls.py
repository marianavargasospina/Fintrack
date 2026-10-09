from fastapi.testclient import TestClient

from app.core.rate_limit import (
    check_login_rate_limit,
    clear_login_attempts,
)
from app.main import app


client = TestClient(app)


def test_health_does_not_expose_environment_or_user_count():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_login_rate_limit_blocks_after_five_attempts():
    key = "test-rate-limit"
    clear_login_attempts(key)

    for _ in range(5):
        check_login_rate_limit(key)

    try:
        check_login_rate_limit(key)
    except Exception as error:
        assert error.status_code == 429
    else:
        raise AssertionError("Expected login rate limit to reject the sixth attempt")
    finally:
        clear_login_attempts(key)
