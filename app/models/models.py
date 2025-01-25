from datetime import datetime
from typing import Dict, List

class User:
    def __init__(self, id: int, name: str, email: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.balance = 0.0

class Transaction:
    def __init__(self, id: int, amount: float, type: str, description: str, user_id: int):
        self.id = id
        self.amount = amount
        self.type = type
        self.description = description
        self.user_id = user_id
        self.timestamp = datetime.now()

# Banco de dados em memória
class Database:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.transactions: Dict[int, Transaction] = {}
        self.user_id_counter = 1
        self.transaction_id_counter = 1

    def create_user(self, name: str, email: str, password: str) -> User:
        user = User(self.user_id_counter, name, email, password)
        self.users[user.id] = user
        self.user_id_counter += 1
        return user

    def get_user_by_email(self, email: str) -> User | None:
        return next((user for user in self.users.values() if user.email == email), None)

    def create_transaction(self, amount: float, type: str, description: str, user_id: int) -> Transaction:
        transaction = Transaction(self.transaction_id_counter, amount, type, description, user_id)
        self.transactions[transaction.id] = transaction
        self.transaction_id_counter += 1
        return transaction

    def get_user_transactions(self, user_id: int) -> List[Transaction]:
        return [t for t in self.transactions.values() if t.user_id == user_id]

# Instância global do "banco de dados"
db = Database() 