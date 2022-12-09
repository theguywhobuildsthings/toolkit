from backend.auth.serve import router as auth_router
from backend.user.serve import router as user_router

from fastapi import Depends, FastAPI
from backend.models.user import user
from backend.db import database
from fastapi.security import OAuth2PasswordBearer

user.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
