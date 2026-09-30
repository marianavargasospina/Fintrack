from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate, AccountOut
from app.services.account_service import AccountService

router = APIRouter(prefix="/accounts", tags=["accounts"])


def get_account_service(db: Session = Depends(get_db)) -> AccountService:
    return AccountService(AccountRepository(db))


@router.get("/", response_model=list[AccountOut])
def list_accounts(
    current_user: User = Depends(get_current_user),
    service: AccountService = Depends(get_account_service),
):
    return service.list_accounts(current_user.id)


@router.post("/", response_model=AccountOut, status_code=201)
def create_account(
    data: AccountCreate,
    current_user: User = Depends(get_current_user),
    service: AccountService = Depends(get_account_service),
):
    return service.create_account(current_user.id, data)