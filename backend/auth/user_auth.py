from backend.models import schemas
from backend.models.user.user_repository import UserRepository
from backend.models.db import User

from passlib.context import CryptContext


class UserAuth:
    username: str
    password: str
    user: User
    context: CryptContext

    def __init__(self, username: str, unhashed_pass: str, user_repo=UserRepository()):
        self.username = username
        self.password = unhashed_pass
        user_repository = user_repo
        self.user = user_repository.get_db_user_by_username(self.username)
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.context.hash(password)

    def __authenticate(self) -> bool:
        return self.verify_password(self.password, self.user.password)

    def get_authenticated_user(self) -> schemas.User:
        if self.user is None or not self.__authenticate():
            return None
        return schemas.User.from_orm(self.user)
