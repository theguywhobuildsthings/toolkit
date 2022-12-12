from typing import Any
import uuid
from fastapi import WebSocket
from backend.models import schemas
from backend.models.db import PairStatus
from backend.models.pair.pair_repository import PairRepository
from backend.redis.redis import RedisMessageThread, ToolkitPubSub
import logging

logger = logging.getLogger('output')

async def handle_ws_request(data, uid: uuid.UUID, user: schemas.User, pair_repo: PairRepository = PairRepository()) -> Any:
    if data and data['type'] == 'request':
        if 'request' in data and 'type' in data['request'] and data['request']['type'] == 'pair-data':
            p = schemas.Pair(user=user, pair_status='unpaired', uuid=str(uid))
            p = pair_repo.create_pair(user, p)
            logger.debug(f"created pair: {p.id} ({p.uuid})")
            return {"message": "pair-info", "data": {"uuid": str(uid), 'pair_url_path': f'/pair/start/{str(uid)}'}}




def pair_handling_factory(websocket: WebSocket):
    async def handle_pairing_message(thread: RedisMessageThread, decoded_data: Any, repo: PairRepository = PairRepository()):
        if decoded_data and 'category' in decoded_data and decoded_data['category'] == 'pairing':
            if 'data' in decoded_data and 'pair_id' in decoded_data['data']:
                logger.debug(f'Received pairing message of type: { decoded_data["category"] } for { str(decoded_data["data"]["pair_id"]) }')
                pair_id = decoded_data["data"]["pair_id"]
                if decoded_data['category'] == 'pairing' and 'message' in decoded_data:
                    if decoded_data['message'] == 'pair-confirm':
                        if repo.update_pair_status(pair_id, PairStatus.paired):
                            await websocket.send_json({"message": 'pair-complete', "pair_id": pair_id})
                        else:
                            await websocket.send_json({"message": 'pair-fail', "pair_id": pair_id})
                    if decoded_data['message'] == 'pair-start':
                        if repo.update_pair_status(pair_id, PairStatus.pair_started):
                            await websocket.send_json({"message": 'pair-start', "pair_id": pair_id})
                        else:
                            await websocket.send_json({"message": 'pair-fail', "pair_id": pair_id})
                    if 'exit_flow' in decoded_data['data'] and decoded_data['data']['exit_flow'] == True:
                        thread.stop()
                        return
    return handle_pairing_message

