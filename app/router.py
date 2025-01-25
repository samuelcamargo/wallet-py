from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .schemas.schemas import UserCreate, UserResponse, TransactionCreate, TransactionResponse, LoginData
from .models.models import db
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = db.get_user_by_email(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.post("/users/", response_model=UserResponse)
def create_user(user_data: UserCreate):
    if db.get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = db.create_user(user_data.name, user_data.email, user_data.password)
    return UserResponse(id=user.id, name=user.name, email=user.email, balance=user.balance)

@router.post("/token")
def login(login_data: LoginData):
    user = db.get_user_by_email(login_data.email)
    if not user or user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": user.email, "token_type": "bearer"}

@router.post("/transactions/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, current_user = Depends(get_current_user)):
    if transaction.type == "withdrawal" and current_user.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    new_transaction = db.create_transaction(
        transaction.amount,
        transaction.type,
        transaction.description,
        current_user.id
    )
    
    if transaction.type == "deposit":
        current_user.balance += transaction.amount
    else:
        current_user.balance -= transaction.amount
        
    return TransactionResponse(
        id=new_transaction.id,
        amount=new_transaction.amount,
        type=new_transaction.type,
        description=new_transaction.description,
        user_id=new_transaction.user_id,
        timestamp=new_transaction.timestamp
    )

@router.get("/transactions/", response_model=List[TransactionResponse])
def get_transactions(current_user = Depends(get_current_user)):
    transactions = db.get_user_transactions(current_user.id)
    return [
        TransactionResponse(
            id=t.id,
            amount=t.amount,
            type=t.type,
            description=t.description,
            user_id=t.user_id,
            timestamp=t.timestamp
        ) for t in transactions
    ]

@router.get("/balance/")
def get_balance(current_user = Depends(get_current_user)):
    return {"balance": current_user.balance} 