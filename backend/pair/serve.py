import uuid
import threading
import logging

from backend.auth.serve import get_current_user
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi import status as http_status
from backend.models.db import User
from backend.models.pair.pair_repository import PairRepository
from backend.models import schemas
from backend.models.user.user_repository import UserRepository
from backend.pair.pair_utils import handle_ws_request, pair_handling_factory
from backend.redis.redis import ToolkitPubSub, RedisMessageThread
from typing import Any

logger = logging.getLogger('output')
router = APIRouter(prefix="/pair")

def ensure_pair_exists(uid: str):
    if not PairRepository().pair_exists(uid):
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Pair request not found",
        )

@router.get("/complete/{uid}")
async def status(uid: str):
    ensure_pair_exists(uid)
    logger.info("Pairing: " + uid)
    pub = ToolkitPubSub()
    await pub.send_message(uid, message=
            {"category": "pairing", "message": "pair-confirm", "data": {"exit_flow": True, "pair_id": uid}}
    )
    return {"status": "success"}

@router.get("/list")
async def list_pairs_for_user(user: schemas.User = Depends(get_current_user)):
    logger.debug(f"Getting list of pairs for user {user.id} ({user.username})")
    return user
    

@router.get("/start/{uid}")
async def status(uid: str):
    ensure_pair_exists(uid)
    logger.info("Pairing: " + uid)
    pub = ToolkitPubSub()
    await pub.send_message(uid, message=
            {"category": "pairing", "message": "pair-start", "data": {"exit_flow": False, "pair_id": uid}}
    )
    return {"status": "success"}

 
@router.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    thread: threading.Thread = None
    user = await get_current_user(token)
    pair_uid = uuid.uuid4()
    try:
        pubsub = ToolkitPubSub()
        thread = pubsub.listen_for_message(str(pair_uid), pair_handling_factory(websocket))
        thread.start()
        await websocket.accept()
        while True:
            data = await websocket.receive_json()
            return_data = await handle_ws_request(data, pair_uid, user)
            if return_data:
                await websocket.send_json(return_data)
    except WebSocketDisconnect:
        logger.debug(f'Received disconnect for {pair_uid}')
    finally:
        try:
            logger.debug(f'Closing Pairing Websocket for {user.id} ({user.username}) - {pair_uid}')
            await websocket.close()
        except Exception as e:
            logger.error("Error while closing websocket")
            logger.error(e)
            pass
        try:
            logger.debug(f'Closing Pairing Thread for {user.id} ({user.username}) - {pair_uid}')
            thread.stop()
        except Exception as e:
            logger.error("Error while killing thread.")
            logger.error(e)
            pass
