from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api import accounts, auth
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

app = FastAPI(
    title="FinTrack API",
    description="API de finanzas personales de FinTrack",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "environment": settings.environment}


@app.get("/health/db", tags=["health"])
def health_check_db(db: Session = Depends(get_db)):
    users_count = db.query(User).count()
    return {"status": "ok", "users_count": users_count}