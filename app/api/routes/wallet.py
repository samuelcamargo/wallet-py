from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.schemas.transaction_schema import TransactionCreate, TransactionResponse
from app.use_cases.wallet_use_case import WalletUseCase
from app.api.dependencies import get_current_user
from app.domain.entities.user import User

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.get("/balance")
def get_balance(current_user: User = Depends(get_current_user)):
    return {"balance": current_user.balance}

@router.post("/transfer", response_model=TransactionResponse)
def transfer_money(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    wallet_service = WalletUseCase(db)
    return wallet_service.transfer_money(
        sender_id=current_user.id,
        receiver_id=transaction.receiver_id,
        amount=transaction.amount
    ) 