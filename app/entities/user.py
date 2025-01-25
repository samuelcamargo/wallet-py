from datetime import datetime
from typing import Optional

class User:
    def __init__(
        self, 
        id: int,
        name: str,
        email: str,
        password_hash: str,
        balance: float = 0.0
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.balance = balance

    def update_balance(self, amount: float) -> None:
        self.balance += amount 