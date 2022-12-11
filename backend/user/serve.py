from datetime import datetime, timedelta
import os

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from backend.auth.user_auth import UserAuth
from backend.models.schemas import UserCreate, User
from backend.models.user.user_repository import UserRepository
from backend.auth.serve import get_current_user

router = APIRouter(prefix="/user",)

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    user_repository = UserRepository()
    user = user_repository.create_user(user)
    return User(username=user.username, id=user.id)

@router.get("/", response_model=User)
async def create_user(user: User = Depends(get_current_user)):
    return User(username=user.username, id=user.id)
