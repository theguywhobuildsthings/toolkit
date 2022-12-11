import uuid
import threading
import logging

from backend.auth.serve import get_current_user
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from backend.models.db import User
from backend.models.pair.pair_repository import PairRepository
from backend.models import schemas
from backend.redis.redis import ToolkitPubSub
from typing import Any
from backend.threading.redis_message_thread import RedisMessageThread

logger = logging.getLogger('output')
router = APIRouter(prefix="/pair")

@router.get("/complete/{uid}")
async def status(uid: str):
    logger.info("Pairing: " + uid)
    pub = ToolkitPubSub()
    await pub.send_message(uid, message=
            {"category": "pairing", "message": "pair-confirm", "data": {"exit_flow": True, "pairing_id": uid}}
    )
    return {"status": "success"}

@router.get("/list")
async def list_pairs_for_user(user: schemas.User = Depends(get_current_user)):
    logger.debug(f"Getting list of pairs for user {user.id} ({user.username})")
    return user.pairs
    

@router.get("/start/{uid}")
async def status(uid: str):
    logger.info("Pairing: " + uid)
    pub = ToolkitPubSub()
    await pub.send_message(uid, message=
            {"category": "pairing", "message": "pair-start", "data": {"exit_flow": False, "pairing_id": uid}}
    )
    return {"status": "success"}

async def handle_ws_request(data, uid: uuid.UUID, user: schemas.User) -> Any:
    if data['type'] == 'request':
        if data['request']['type'] == 'pair-data':
            repo = PairRepository()
            p = schemas.Pair(user=user, pair_status='unpaired', uuid=str(uid))
            p = repo.create_pair(user, p)
            logger.debug(f"created pair: {p.id} ({p.uuid})")
            return {"message": "pair-info", "data": {"uuid": str(uid), 'pair_url_path': f'/pair/start/{str(uid)}'}}

 
@router.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    thread: threading.Thread = None
    user = await get_current_user(token)
    pair_uid = uuid.uuid4()
    async def handle_pairing_message(thread: RedisMessageThread, decoded_data: Any):
        logger.debug(f'Received pairing message for { decoded_data["data"]["pairing_id"] }')
        if decoded_data['category'] == 'pairing':
            if decoded_data['message'] == 'pair-confirm':
                await websocket.send_json({"message": 'pair-complete'})
            if decoded_data['message'] == 'pair-start':
                await websocket.send_json({"message": 'pair-start'})
            if 'data' in decoded_data and 'exit_flow' in decoded_data['data'] and decoded_data['data']['exit_flow'] == True:
                thread.stop()
                return
    try:
        pubsub = ToolkitPubSub()
        thread = pubsub.listen_for_message(str(pair_uid), handle_pairing_message)
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
        except:
            pass
        try:
            logger.debug(f'Closing Pairing Thread for {user.id} ({user.username}) - {pair_uid}')
            thread.stop()
        except Exception as e:
            logger.error(e)
            pass
