from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def list_categories(self, user_id):
        return self.repository.list_by_user(user_id)

    def get_category(self, user_id, category_id):
        return self.repository.get_by_id(user_id, category_id)

    def create_category(self, user_id, data: CategoryCreate):
        return self.repository.create(user_id, data)

    def update_category(self, user_id, category_id, data: CategoryUpdate):
        category = self.repository.get_by_id(user_id, category_id)
        if category is None:
            return None
        return self.repository.update(user_id, category, data)

    def delete_category(self, user_id, category_id):
        category = self.repository.get_by_id(user_id, category_id)
        if category is None:
            return False
        self.repository.delete(user_id, category)
        return True