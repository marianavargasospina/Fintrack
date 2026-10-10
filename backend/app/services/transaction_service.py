from math import ceil

from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def _validate_references(self, user_id, data):
        account = self.repository.get_account(user_id, data.account_id)
        if account is None:
            raise ValueError("La cuenta de origen no pertenece al usuario")

        if data.destination_account_id is not None:
            destination = self.repository.get_account(
                user_id, data.destination_account_id
            )
            if destination is None:
                raise ValueError("La cuenta destino no pertenece al usuario")

        if data.category_id is not None:
            category = self.repository.get_category(user_id, data.category_id)
            if category is None:
                raise ValueError("La categoría no pertenece al usuario")
            if category.type != data.type:
                raise ValueError("La categoría no coincide con el tipo de transacción")

    def list_transactions(self, user_id, **filters):
        items, total = self.repository.list_by_user(user_id, **filters)
        page = filters["page"]
        page_size = filters["page_size"]
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": ceil(total / page_size) if total else 0,
        }

    def get_transaction(self, user_id, transaction_id):
        return self.repository.get_by_id(user_id, transaction_id)

    def create_transaction(self, user_id, data: TransactionCreate):
        self._validate_references(user_id, data)
        return self.repository.create(user_id, data)

    def update_transaction(self, user_id, transaction_id, data: TransactionUpdate):
        self._validate_references(user_id, data)
        return self.repository.update(user_id, transaction_id, data)

