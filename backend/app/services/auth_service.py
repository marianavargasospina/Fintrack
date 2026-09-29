from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, data: UserCreate):
        if self.repository.get_by_email(data.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cuenta registrada con ese correo.",
            )
        return self.repository.create(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
        )

    def authenticate(self, data: UserLogin) -> str:
        user = self.repository.get_by_email(data.email)
        if user is None or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas.",
            )
        return create_access_token(user.id)