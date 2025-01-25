from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    balance: float

class TransactionCreate(BaseModel):
    amount: float
    type: str
    description: Optional[str] = None

    @validator('type')
    def validate_type(cls, v):
        if v not in ['deposit', 'withdrawal']:
            raise ValueError('Transaction type must be deposit or withdrawal')
        return v

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    description: Optional[str]
    user_id: int
    timestamp: datetime

class LoginData(BaseModel):
    email: str
    password: str 