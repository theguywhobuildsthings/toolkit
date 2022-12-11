from typing import Any
import uuid
from fastapi import WebSocket
from backend.models import schemas
from backend.models.pair.pair_repository import PairRepository
from backend.redis.redis import RedisMessageThread, ToolkitPubSub
import logging

logger = logging.getLogger('output')

async def handle_ws_request(data, uid: uuid.UUID, user: schemas.User, pair_repo: PairRepository = PairRepository()) -> Any:
    if data['type'] == 'request':
        if data['request']['type'] == 'pair-data':
            p = schemas.Pair(user=user, pair_status='unpaired', uuid=str(uid))
            p = pair_repo.create_pair(user, p)
            logger.debug(f"created pair: {p.id} ({p.uuid})")
            return {"message": "pair-info", "data": {"uuid": str(uid), 'pair_url_path': f'/pair/start/{str(uid)}'}}

def pair_handling_factory(websocket: WebSocket):
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
    return handle_pairing_message

