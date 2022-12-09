from sqlalchemy.orm import Session

from .user import User
from .user_schemas import UserCreate
from backend.db import database 
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def get_user_by_username(self, username: str) -> User:
        db = database.SessionLocal()
        user: User = None
        try:
            user = db.query(User).filter(User.username == username).first()
        finally:
            db.close()
        return user

    def create_user(self, user: UserCreate) -> User:
        db = database.SessionLocal()
        try:
            hashed_password = pwd_context.hash(user.password)
            db_user = User(username=user.username, password=hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        finally:
            db.close()
        return db_user
