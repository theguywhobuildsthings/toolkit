from typing import Any, Optional, List
from pydantic import BaseModel

from backend.models.db import PairStatus

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class Pair(BaseModel):
    id: Optional[int]
    uuid: str
    pair_status: PairStatus
    
    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    pairs: List[Pair]

    class Config:
        orm_mode = True


