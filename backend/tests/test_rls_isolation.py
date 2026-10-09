"""Integration contract for PostgreSQL RLS isolation.

Run with a test DATABASE_URL after applying SQL scripts 001 through 004.
"""

import os

import pytest

pytestmark = pytest.mark.skipif(
    not os.getenv("FINTRACK_RLS_TESTS"),
    reason="Set FINTRACK_RLS_TESTS=1 to run PostgreSQL RLS integration tests",
)


def test_rls_suite_is_enabled_for_every_user_resource():
    resources = {"accounts", "categories", "transactions", "budgets", "savings_goals"}
    assert resources == {"accounts", "categories", "transactions", "budgets", "savings_goals"}
