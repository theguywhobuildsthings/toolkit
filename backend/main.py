from backend.auth.serve import router as auth_router
from backend.user.serve import router as user_router
from backend.pair.serve import router as pair_router

from fastapi import Depends, FastAPI
from backend.models.user import user
from backend.db import database
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

user.Base.metadata.create_all(bind=database.engine)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(pair_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
