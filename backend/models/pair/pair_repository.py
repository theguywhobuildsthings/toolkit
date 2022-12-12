
import logging
import uuid

from sqlalchemy.orm import Session
from backend.models import db
from backend.models.db import PairStatus, User, Pair
from backend.db import database
from backend.models import schemas


logger = logging.getLogger('output')

class PairRepository:
    def get_pair_by_uuid(self, uuid: uuid.UUID) -> schemas.Pair:
        db = database.SessionLocal()
        db_pair: db.Pair = None
        try:
            db_pair = db.query(Pair).filter(Pair.uuid == uuid).first()
        finally:
            db.close()
        user = schemas.Pair.from_orm(db_pair)
        return user
        
    def create_pair(self, user: schemas.User, pair: schemas.Pair) -> schemas.Pair:
        logger.debug(f'Creating pair for user: {user.id} ({user.username}) - {pair.uuid}: {pair.pair_status}')
        conn = database.SessionLocal()
        try:
            db_user = self.__get_user_by_id(conn, user.id)
            db_pair = db.Pair(uuid=pair.uuid, user=db_user, pair_status=pair.pair_status)
            db_user.pairs.append(db_pair)
            conn.add(db_pair)
            conn.merge(db_user)
            conn.commit()
            conn.refresh(db_pair)
        finally:
            conn.close()
        return schemas.Pair.from_orm(db_pair)
        
    def __get_user_by_id(self, conn: database.SessionLocal, user_id: schemas.User) -> db.User:
        db_user: db.User = None
        try:
            db_user = conn.query(User).filter(User.id == user_id).first()
        finally:
            conn.close()
        return db_user

    def __update_status(self, uuid: uuid.UUID, status: PairStatus) -> schemas.Pair:
        conn = database.SessionLocal()
        db_pair: db.Pair = None
        try:
            db_pair = conn.query(Pair).filter(Pair.uuid == str(uuid)).first()
            if not db_pair:
                return None
            db_pair.pair_status = status
            conn.merge(db_pair)
            conn.commit()
            conn.refresh(db_pair)
        finally:
            conn.close()
        return schemas.Pair.from_orm(db_pair)

    def update_pair_status(self, pair_id: str, status: PairStatus) -> bool:
        if self.__update_status(pair_id, status):
            return True
        else:
            try:
                self.__update_status(pair_id, PairStatus.failed)
            finally:
                return False

    def pair_exists(self, uuid: str) -> bool:
        conn = database.SessionLocal()
        db_pair: db.Pair = None
        try:
            db_pair = conn.query(Pair).filter(Pair.uuid == str(uuid)).first()
            if not db_pair:
                return False
            return True
        finally:
            conn.close()