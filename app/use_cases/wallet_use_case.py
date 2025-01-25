from app.repositories.user_repository import UserRepository
from app.repositories.transaction_repository import TransactionRepository
from app.entities.transaction import Transaction
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

class WalletUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        transaction_repository: TransactionRepository,
        db: Session
    ):
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository
        self.db = db

    def get_balance(self, user_id: int) -> float:
        user = self._get_user_or_raise(user_id)
        return user.balance

    def deposit(self, user_id: int, amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("Amount must be positive")
            
        user = self._get_user_or_raise(user_id)
        user.update_balance(amount)
        self.user_repository.update(user)
        
        transaction = Transaction(
            id=0,
            amount=amount,
            sender_id=user_id,
            receiver_id=user_id,
            transaction_type="deposit"
        )
        return self.transaction_repository.create(transaction)

    def transfer(self, sender_id: int, receiver_id: int, amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("Amount must be positive")
            
        sender = self._get_user_or_raise(sender_id)
        receiver = self._get_user_or_raise(receiver_id)
        
        if sender.balance < amount:
            raise ValueError("Insufficient funds")
            
        sender.update_balance(-amount)
        receiver.update_balance(amount)
        
        self.user_repository.update(sender)
        self.user_repository.update(receiver)
        
        transaction = Transaction(
            id=0,
            amount=amount,
            sender_id=sender_id,
            receiver_id=receiver_id,
            transaction_type="transfer"
        )
        return self.transaction_repository.create(transaction)

    def list_transactions(
        self,
        user_id: int,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[Transaction]:
        self._get_user_or_raise(user_id)
        return self.transaction_repository.get_by_user_id(user_id, start_date, end_date)

    def _get_user_or_raise(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def transfer_money(self, sender_id: int, receiver_id: int, amount: float):
        sender = self.db.query(User).filter(User.id == sender_id).first()
        receiver = self.db.query(User).filter(User.id == receiver_id).first()

        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver not found")

        if sender.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        sender.balance -= amount
        receiver.balance += amount

        transaction = Transaction(
            amount=amount,
            sender_id=sender_id,
            receiver_id=receiver_id
        )

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        
        return transaction 