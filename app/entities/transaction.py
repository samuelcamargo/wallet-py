from datetime import datetime

class Transaction:
    def __init__(
        self,
        id: int,
        amount: float,
        sender_id: int,
        receiver_id: int,
        transaction_type: str,
        created_at: datetime = datetime.now()
    ):
        self.id = id
        self.amount = amount
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.transaction_type = transaction_type
        self.created_at = created_at 