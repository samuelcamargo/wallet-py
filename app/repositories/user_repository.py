from app.entities.user import User
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self):
        self.users = {}
        self.current_id = 1

    def create(self, user: User) -> User:
        user.id = self.current_id
        self.users[self.current_id] = user
        self.current_id += 1
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return next(
            (user for user in self.users.values() if user.email == email),
            None
        )

    def update(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def update_user(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user 