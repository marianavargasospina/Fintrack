from datetime import date
from decimal import Decimal
from uuid import uuid4

from app.services.dashboard_service import DashboardService


class FakeDashboardRepository:
    def summary(self, user_id, month):
        return (
            {"income": Decimal("100"), "expense": Decimal("40")},
            [{"category_id": uuid4(), "name": "Food", "amount": Decimal("40")}],
            [{"month": date(2026, 10, 1), "income": Decimal("100"), "expense": Decimal("40")}],
            {"balance": Decimal("60")},
        )


def test_dashboard_service_preserves_sql_aggregate_results():
    result = DashboardService(FakeDashboardRepository()).summary(uuid4(), date(2026, 10, 1))
    assert result["income"] == Decimal("100")
    assert result["expense"] == Decimal("40")
    assert result["total_balance"] == Decimal("60")
    assert result["expenses_by_category"][0]["name"] == "Food"
