import logging

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limit import check_login_rate_limit, clear_login_attempts
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserCreate, UserLogin, UserOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, service: AuthService = Depends(get_auth_service)):
    return service.register(data)


@router.post("/login", response_model=Token)
def login(
    data: UserLogin,
    request: Request,
    service: AuthService = Depends(get_auth_service),
):
    client_key = request.client.host if request.client else "unknown"
    check_login_rate_limit(client_key)
    try:
        access_token = service.authenticate(data)
    except Exception:
        logger.warning("Failed login attempt for email=%s from ip=%s", data.email, client_key)
        raise
    clear_login_attempts(client_key)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user