import enum
import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, Mapped, validates

from backend.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    pairs: Mapped[list["Pair"]] = relationship(
        "Pair", back_populates="user", lazy="immediate"
    )

    @validates("username")
    def validate_username(self, key, value):
        if " " in value:
            raise ValueError("Username should not contain spaces")
        if len(value) > 50:
            raise ValueError("Username should not be longer than 50 chars")
        return value


class PairStatus(enum.Enum):
    unpaired = "unpaired"
    pair_started = "pair_started"
    paired = "paired"
    failed = "failed"


class Pair(Base):
    __tablename__ = "pair"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="pairs", lazy="immediate")
    pair_status = Column(Enum(PairStatus))
    username = Column(String, nullable=True)

    @validates("uuid")
    def validate_uuid(self, key, value):
        uuid.UUID(value, version=4)
        if self.uuid:
            raise ValueError("uuid cannot be modified.")

        return value
