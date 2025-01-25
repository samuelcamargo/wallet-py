from app.entities.transaction import Transaction
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas.transaction_schema import TransactionCreate

class TransactionRepository:
    def __init__(self):
        self.transactions = {}
        self.current_id = 1

    def create(self, transaction: Transaction) -> Transaction:
        transaction.id = self.current_id
        self.transactions[self.current_id] = transaction
        self.current_id += 1
        return transaction

    def get_by_user_id(self, user_id: int, start_date: datetime = None, end_date: datetime = None) -> List[Transaction]:
        transactions = [
            t for t in self.transactions.values()
            if t.sender_id == user_id or t.receiver_id == user_id
        ]
        
        if start_date:
            transactions = [t for t in transactions if t.created_at >= start_date]
        if end_date:
            transactions = [t for t in transactions if t.created_at <= end_date]
            
        return transactions

    def create_transaction(self, db: Session, transaction: TransactionCreate, user_id: int) -> Transaction:
        db_transaction = Transaction(
            amount=transaction.amount,
            type=transaction.type,
            description=transaction.description,
            user_id=user_id
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction 