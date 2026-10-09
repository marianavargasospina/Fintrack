from datetime import date

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, repository: DashboardRepository):
        self.repository = repository

    def summary(self, user_id, month: date):
        totals, categories, months, balance = self.repository.summary(user_id, month)
        return {
            "month": month,
            "income": totals["income"],
            "expense": totals["expense"],
            "total_balance": balance["balance"],
            "expenses_by_category": [dict(row) for row in categories],
            "last_six_months": [dict(row) for row in months],
        }