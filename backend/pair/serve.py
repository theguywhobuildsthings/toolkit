from datetime import datetime, timedelta
import os
import asyncio
import uuid

from backend.auth.serve import get_current_user
from fastapi import APIRouter, WebSocket
from backend.models.user.user_schemas import User
# from backend.pair.utils import handle_ws_request
from backend.redis.redis import ToolkitPubSub
import json 

router = APIRouter(prefix="/pair")

@router.get("/{uid}")
async def status(uid: str):
    print("Pairing: " + uid)
    pub = ToolkitPubSub()
    await pub.send_message(uid, message={"message": "pair-confirm", "exit_flow": True})
    return {"status": "success"}
    # pairing_uid = uuid.UUID(uid)



async def handle_ws_request(data, websocket: WebSocket):
    uid = uuid.uuid4()
    if data['type'] == 'request':
        if data['request']['type'] == 'pair-data':
            #subscribe to redis service

            pubsub = ToolkitPubSub()
            pubsub.listen_for_message(str(uid), lambda x: websocket.send_json({"message": 'pair-complete'}))
            return {"message": "pair-info", "data": {"uuid": str(uid), 'pair_url_path': f'/pair/{str(uid)}'}}


@router.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        user = await get_current_user(token)
        await websocket.accept()
        while True:
            data = await websocket.receive_json()
            return_data = await handle_ws_request(data, websocket)
            if return_data:
                await websocket.send_json(return_data)
    finally:
        try:
            await websocket.close()
        except:
            pass
