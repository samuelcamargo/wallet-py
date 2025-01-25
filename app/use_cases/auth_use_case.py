from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.infrastructure.config import settings
from app.schemas.user_schema import UserCreate
from app.domain.entities.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthUseCase:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def register_user(self, user: UserCreate):
        db_user = User(
            email=user.email,
            hashed_password=pwd_context.hash(user.password),
            full_name=user.full_name,
            balance=0.0
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, email: str, password: str):
        user = self.get_user_by_email(email)
        if not user or not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=400,
                detail="Incorrect email or password"
            )
        access_token = self.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt 