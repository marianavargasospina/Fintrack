"""Integration test for PostgreSQL RLS isolation."""

import os
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text

pytestmark = pytest.mark.skipif(
    not os.getenv("FINTRACK_RLS_TESTS"),
    reason="Set FINTRACK_RLS_TESTS=1 to run PostgreSQL RLS integration tests",
)


def test_accounts_are_isolated_between_users():
    database_url = os.environ["DATABASE_URL"]
    engine = create_engine(database_url)
    first_user = uuid4()
    second_user = uuid4()

    try:
        with engine.begin() as connection:
            connection.execute(
                text("INSERT INTO users (id, name, email, password_hash) VALUES (:id, :name, :email, :password_hash)"),
                [
                    {"id": first_user, "name": "First", "email": f"{first_user}@example.com", "password_hash": "test"},
                    {"id": second_user, "name": "Second", "email": f"{second_user}@example.com", "password_hash": "test"},
                ],
            )
            connection.execute(
                text("INSERT INTO accounts (user_id, name, type, currency) VALUES (:user_id, :name, 'cash', 'COP')"),
                [
                    {"user_id": first_user, "name": "First account"},
                    {"user_id": second_user, "name": "Second account"},
                ],
            )
            connection.execute(
                text("SELECT set_config('app.current_user_id', :user_id, true)"),
                {"user_id": str(first_user)},
            )
            rows = connection.execute(text("SELECT user_id FROM accounts")).all()
            assert rows == [(first_user,)]
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM users WHERE id IN (:first_user, :second_user)"),
                {"first_user": first_user, "second_user": second_user},
            )
        engine.dispose()
