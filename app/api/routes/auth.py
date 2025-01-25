from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.schemas.user_schema import UserCreate, UserResponse, Token
from app.use_cases.auth_use_case import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthUseCase(db)
    return auth_service.register_user(user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_service = AuthUseCase(db)
    return auth_service.authenticate_user(form_data.username, form_data.password) 