from app.repositories.transaction_repository import TransactionRepository


class ExportService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def transactions(self, user_id, **filters):
        items, _ = self.repository.list_by_user(
            user_id, page=1, page_size=1_000_000, **filters
        )
        return items