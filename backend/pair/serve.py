from datetime import datetime, timedelta
import os
import asyncio
from typing import Any, Tuple
import uuid
import threading

from backend.auth.serve import get_current_user
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.models.user.user_schemas import User
# from backend.pair.utils import handle_ws_request
from backend.redis.redis import ToolkitPubSub
import json

from backend.threading.stoppable_thread import StoppableThread 

router = APIRouter(prefix="/pair")

@router.get("/{uid}")
async def status(uid: str):
    print("Pairing: " + uid)
    pub = ToolkitPubSub()
    await pub.send_message(uid, message={"message": "pair-confirm", "exit_flow": True})
    return {"status": "success"}
    # pairing_uid = uuid.UUID(uid)

async def handle_ws_request(data, uid: uuid.UUID, websocket: WebSocket) -> Any:
    if data['type'] == 'request':
        if data['request']['type'] == 'pair-data':
            #subscribe to redis service
            return {"message": "pair-info", "data": {"uuid": str(uid), 'pair_url_path': f'/pair/{str(uid)}'}}


@router.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    thread: threading.Thread = None
    try:
        
        user = await get_current_user(token)
        pair_uid = uuid.uuid4()
        pubsub = ToolkitPubSub()
        thread = pubsub.listen_for_message(str(pair_uid), lambda x: websocket.send_json({"message": 'pair-complete'}))
        thread.start()
        print(f'Thread: {str(thread)}')
        await websocket.accept()
        while True:
            data = await websocket.receive_json()
            return_data = await handle_ws_request(data, pair_uid, websocket)
            if return_data:
                await websocket.send_json(return_data)
    except WebSocketDisconnect:
        pass
    finally:
        try:
            print("Closing websocket")
            await websocket.close()
        except:
            pass
        try:
            print("Killing thread")
            thread.stop()
        except Exception as e:
            print(e)
            pass
