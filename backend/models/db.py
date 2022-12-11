import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, Mapped

from backend.db.database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    pairs: Mapped[list["Pair"]] = relationship("Pair", back_populates="user", lazy='immediate')

class PairStatus(enum.Enum):
    unpaired = 'unpaired'
    pair_started = 'pair_started'
    paired = 'paired'

class Pair(Base):
    __tablename__ = "pair"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="pairs", lazy='immediate')
    pair_status = Column(Enum(PairStatus))

