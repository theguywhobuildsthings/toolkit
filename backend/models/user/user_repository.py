import logging
from pydantic import ValidationError

from sqlalchemy.orm import Session
from backend.models.db import User
from backend.db import database
from passlib.context import CryptContext
from backend.models import schemas

logger = logging.getLogger("output")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def get_user_by_username(self, username: str) -> schemas.User:
        try:
            return schemas.User.from_orm(self.get_db_user_by_username(username))
        except ValidationError:
            return None

    def get_db_user_by_username(self, username: str) -> schemas.User:
        logger.debug(f"Getting db user by username: {username}")
        db = database.SessionLocal()
        user: User = None
        try:
            user = db.query(User).filter(User.username == username).first()
            if user:
                logger.debug(f"Found user: {username}({user.id})")
                return user
        finally:
            db.close()
        logger.debug(f"Could not find user: {username}")

    def create_user(self, user: schemas.UserCreate) -> schemas.User:
        db = database.SessionLocal()
        try:
            hashed_password = pwd_context.hash(user.password)
            db_user = User(username=user.username.lower(), password=hashed_password)
            db_user.pairs = []
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        finally:
            db.close()
        return db_user
