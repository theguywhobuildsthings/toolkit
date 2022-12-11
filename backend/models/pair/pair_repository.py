
import logging
import uuid

from sqlalchemy.orm import Session
from backend.models import db
from backend.models.db import User, Pair
from backend.db import database
from backend.models import schemas


logger = logging.getLogger('output')

def __schema_pair_from_db_pair(db_pair: Pair) -> schemas.Pair:
    db = database.SessionLocal()
    try:
        db_user: db.User = db_pair.user
        schema_user = schemas.User(id=db_user.id, username=db_user.username)
        for db_pair in db_user.pairs:
            schema_pair = schemas.Pair(id=db_pair.id, uuid=db_pair.uuid, user=schema_user, pair_status=db_pair.status)
            schema_user.pairs.append(schema_pair)
        return schema_pair
    finally:
        db.close()

class PairRepository:
    def get_pair_by_uuid(self, uuid: uuid.UUID) -> schemas.Pair:
        db = database.SessionLocal()
        db_pair: db.Pair = None
        try:
            db_pair = db.query(Pair).filter(Pair.uuid == uuid).first()
        finally:
            db.close()
        user = __schema_pair_from_db_pair(db_pair)
        return user
        
    def create_pair(self, user: schemas.User, pair: schemas.Pair) -> schemas.Pair:
        logger.debug(f'Creating pair for user: {user.id} ({user.username}) - {pair.uuid}')
        conn = database.SessionLocal()
        try:
            db_user = self.__get_user_by_id(conn, user.id)
            logger.debug(db_user.username)
            db_pair = db.Pair(uuid=pair.uuid, user=db_user, status=pair.pair_status)
            db_user.pairs.append(db_pair)
            conn.add(db_pair)
            conn.merge(db_user)
            conn.commit()
            conn.refresh(db_pair)
        finally:
            conn.close()
        return schemas.Pair(id=db_pair.id, uuid=db_pair.uuid, user=user, pair_status=db_pair.status)
        
    def __get_user_by_id(self, conn: database.SessionLocal, user_id: schemas.User) -> db.User:
        db_user: db.User = None
        try:
            db_user = conn.query(User).filter(User.id == user_id).first()
        finally:
            conn.close()
        return db_user
