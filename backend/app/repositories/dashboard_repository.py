from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Session


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def summary(self, user_id, month: date):
        self.db.execute(
            text("SELECT set_config('app.current_user_id', :uid, true)"),
            {"uid": str(user_id)},
        )
        totals = self.db.execute(text("""
            SELECT
                COALESCE(SUM(amount) FILTER (WHERE type = 'income'), 0) AS income,
                COALESCE(SUM(amount) FILTER (WHERE type = 'expense'), 0) AS expense
            FROM transactions
            WHERE user_id = :user_id
              AND transaction_date >= date_trunc('month', CAST(:month AS date))
              AND transaction_date < date_trunc('month', CAST(:month AS date)) + interval '1 month'
        """), {"user_id": user_id, "month": month}).mappings().one()
        categories = self.db.execute(text("""
            SELECT c.id AS category_id, c.name, COALESCE(SUM(t.amount), 0) AS amount
            FROM transactions t JOIN categories c ON c.id = t.category_id
            WHERE t.user_id = :user_id AND t.type = 'expense'
              AND t.transaction_date >= date_trunc('month', CAST(:month AS date))
              AND t.transaction_date < date_trunc('month', CAST(:month AS date)) + interval '1 month'
            GROUP BY c.id, c.name ORDER BY amount DESC
        """), {"user_id": user_id, "month": month}).mappings().all()
        months = self.db.execute(text("""
            SELECT date_trunc('month', month)::date AS month,
                   COALESCE(SUM(t.amount) FILTER (WHERE t.type = 'income'), 0) AS income,
                   COALESCE(SUM(t.amount) FILTER (WHERE t.type = 'expense'), 0) AS expense
            FROM generate_series(
                date_trunc('month', CAST(:month AS date)) - interval '5 months',
                date_trunc('month', CAST(:month AS date)), interval '1 month'
            ) AS month
            LEFT JOIN transactions t ON t.user_id = :user_id
                AND date_trunc('month', t.transaction_date) = date_trunc('month', month)
            GROUP BY month ORDER BY month
        """), {"user_id": user_id, "month": month}).mappings().all()
        balance = self.db.execute(text("""
            SELECT COALESCE(SUM(current_balance), 0) AS balance
            FROM accounts WHERE user_id = :user_id
        """), {"user_id": user_id}).mappings().one()
        return totals, categories, months, balance