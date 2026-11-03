from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def list_accounts(self, user_id):
        return self.repository.list_by_user(user_id)

    def create_account(self, user_id, data: AccountCreate):
        return self.repository.create(user_id, data)

    def delete_account(self, user_id, account_id):
        return self.repository.delete(user_id, account_id)