from backend.auth.serve import router as auth_router
from backend.user.serve import router as user_router
from backend.pair.serve import router as pair_router

from fastapi import FastAPI
from backend.models import db
from backend.db import database
from fastapi.middleware.cors import CORSMiddleware
import logging

db.Base.metadata.create_all(bind=database.engine)


def setup_custom_logger():
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger("output")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.info("Initialized App")


origins = [
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

setup_custom_logger()
