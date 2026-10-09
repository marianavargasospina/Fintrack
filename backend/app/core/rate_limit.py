from collections import defaultdict
from threading import Lock
from time import monotonic

from fastapi import HTTPException, status

_LOGIN_WINDOW_SECONDS = 300
_LOGIN_MAX_ATTEMPTS = 5
_attempts: dict[str, list[float]] = defaultdict(list)
_lock = Lock()


def check_login_rate_limit(key: str) -> None:
    now = monotonic()
    with _lock:
        recent_attempts = [
            timestamp
            for timestamp in _attempts[key]
            if now - timestamp < _LOGIN_WINDOW_SECONDS
        ]
        _attempts[key] = recent_attempts
        if len(recent_attempts) >= _LOGIN_MAX_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos de inicio de sesión. Inténtalo más tarde.",
                headers={"Retry-After": str(_LOGIN_WINDOW_SECONDS)},
            )
        recent_attempts.append(now)


def clear_login_attempts(key: str) -> None:
    with _lock:
        _attempts.pop(key, None)
