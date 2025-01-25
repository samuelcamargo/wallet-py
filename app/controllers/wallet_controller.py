from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreate, UserResponse, TokenResponse
from app.schemas.transaction_schema import TransferCreate, DepositCreate, TransactionResponse, TransactionCreate
from app.use_cases.auth_use_case import AuthUseCase
from app.use_cases.wallet_use_case import WalletUseCase
from app.repositories.user_repository import UserRepository
from app.repositories.transaction_repository import TransactionRepository
from datetime import datetime
import jwt
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db

router = APIRouter(prefix="/api", tags=["wallet"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Repositories (simulando injeção de dependência)
user_repository = UserRepository()
transaction_repository = TransactionRepository()

def get_auth_use_case():
    return AuthUseCase(user_repository)

def get_wallet_use_case():
    return WalletUseCase(user_repository, transaction_repository)

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, AuthUseCase.SECRET_KEY, algorithms=["HS256"])
        return int(payload["sub"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# Rotas de autenticação
@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, use_case: AuthUseCase = Depends(get_auth_use_case)):
    try:
        user = use_case.create_user(user_data.name, user_data.email, user_data.password)
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            balance=user.balance
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: AuthUseCase = Depends(get_auth_use_case)
):
    try:
        token = use_case.authenticate(form_data.username, form_data.password)
        return TokenResponse(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# Rotas da carteira
@router.get("/balance", response_model=float)
async def get_balance(
    current_user_id: int = Depends(get_current_user_id),
    use_case: WalletUseCase = Depends(get_wallet_use_case)
):
    try:
        return use_case.get_balance(current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/deposit", response_model=TransactionResponse)
async def deposit(
    deposit_data: DepositCreate,
    current_user_id: int = Depends(get_current_user_id),
    use_case: WalletUseCase = Depends(get_wallet_use_case)
):
    try:
        transaction = use_case.deposit(current_user_id, deposit_data.amount)
        return TransactionResponse(
            id=transaction.id,
            amount=transaction.amount,
            sender_id=transaction.sender_id,
            receiver_id=transaction.receiver_id,
            transaction_type=transaction.transaction_type,
            created_at=transaction.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/transfer", response_model=TransactionResponse)
async def transfer(
    transfer_data: TransferCreate,
    current_user_id: int = Depends(get_current_user_id),
    use_case: WalletUseCase = Depends(get_wallet_use_case)
):
    try:
        transaction = use_case.transfer(
            current_user_id,
            transfer_data.receiver_id,
            transfer_data.amount
        )
        return TransactionResponse(
            id=transaction.id,
            amount=transaction.amount,
            sender_id=transaction.sender_id,
            receiver_id=transaction.receiver_id,
            transaction_type=transaction.transaction_type,
            created_at=transaction.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/transactions", response_model=list[TransactionResponse])
async def list_transactions(
    start_date: datetime = None,
    end_date: datetime = None,
    current_user_id: int = Depends(get_current_user_id),
    use_case: WalletUseCase = Depends(get_wallet_use_case)
):
    try:
        transactions = use_case.list_transactions(current_user_id, start_date, end_date)
        return [
            TransactionResponse(
                id=t.id,
                amount=t.amount,
                sender_id=t.sender_id,
                receiver_id=t.receiver_id,
                transaction_type=t.transaction_type,
                created_at=t.created_at
            )
            for t in transactions
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/transactions/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if transaction.type == 'withdrawal' and current_user.balance < transaction.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds"
        )
    
    transaction_repo = TransactionRepository()
    new_transaction = transaction_repo.create_transaction(db, transaction, current_user.id)
    
    # Atualizar o saldo do usuário
    if transaction.type == 'deposit':
        current_user.balance += transaction.amount
    else:
        current_user.balance -= transaction.amount
    
    db.commit()
    
    return new_transaction 