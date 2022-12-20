from fastapi import Depends, APIRouter, HTTPException, status
from backend.models.schemas import UserCreate, User
from backend.models.user.user_repository import UserRepository
from backend.auth.serve import get_current_user

router = APIRouter(
    prefix="/user",
)


@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    try:
        user_repository = UserRepository()
        user = user_repository.create_user(user)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot create user, {e.args}",
        )


@router.get("/", response_model=User)
async def show_user(user: User = Depends(get_current_user)):
    try:
        return User(username=user.username, id=user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )
