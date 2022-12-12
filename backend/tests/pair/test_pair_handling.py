# def pair_handling_factory(websocket: WebSocket):
#     async def handle_pairing_message(thread: RedisMessageThread, decoded_data: Any):
#         print(decoded_data)
#         if decoded_data and 'category' in decoded_data and decoded_data['category'] == 'pairing':
#             if 'data' in decoded_data and 'pairing_id' in decoded_data['data']:
#                 logger.debug(f'Received pairing message of type: { decoded_data["category"] }')
#                 print(f'Received pairing message of type: { decoded_data["category"] }')
#                 if decoded_data['category'] == 'pairing':
#                     if decoded_data['message'] == 'pair-confirm':
#                         await websocket.send_json({"message": 'pair-complete'})
#                     if decoded_data['message'] == 'pair-start':
#                         await websocket.send_json({"message": 'pair-start'})
#                     if 'exit_flow' in decoded_data['data'] and decoded_data['data']['exit_flow'] == True:
#                         thread.stop()
#                         return
#     return handle_pairing_message

# {
#     "category": "pairing", 
#     "message": "pair-start",
#     "data": {
#         "exit_flow": false, 
#         "pairing_id": "b6cfe20c-c938-47a2-94c7-5cc4ebac8d91"
#     }
# }

from unittest.mock import Mock
import pytest
import websockets
from backend.pair.pair_utils import pair_handling_factory
from backend.tests.utils.redis import RedisMessageThreadMock, make_coroutine

from backend.tests.utils.websocket import WebsocketMock

socket = WebsocketMock()
mock_thread = RedisMessageThreadMock()

@pytest.mark.asyncio
async def test_invalid_data_is_ignored():
    m = Mock()
    socket.send_json = make_coroutine(m)
    pair_handler = pair_handling_factory(socket)

    # Empty
    await pair_handler(mock_thread, {})
    # completely invalid
    await pair_handler(mock_thread, {'bad': 'data'})
    # Has correct category and message but doesn't carry data
    await pair_handler(mock_thread, {'category': 'pairing', 'message': 'pair-start'})
    # Has correct category and message but doesn't carry data
    await pair_handler(mock_thread, {'category': 'pairing', 'message': 'pair-start', 'data': {'bad': "data"}})
    # Has correct data and category with no message
    await pair_handler(mock_thread, {'category': 'pairing', 'data': {'pairing_id': "poop"}})

    m.assert_not_called()

@pytest.mark.asyncio
async def test_valid_confirm_calls_websocket():
    m = Mock()
    socket.send_json = make_coroutine(m)
    pair_handler = pair_handling_factory(socket)
    await pair_handler(mock_thread, {'category': 'pairing', 'message': 'pair-confirm', 'data': {'pairing_id': "poop"}})

    m.assert_called_once_with({"message": 'pair-complete'})

@pytest.mark.asyncio
async def test_valid_start_calls_websocket():
    m = Mock()
    socket.send_json = make_coroutine(m)
    pair_handler = pair_handling_factory(socket)
    await pair_handler(mock_thread, {'category': 'pairing', 'message': 'pair-start', 'data': {'pairing_id': "poop"}})

    m.assert_called_once_with({"message": 'pair-start'})

@pytest.mark.asyncio
async def test_valid_exit_kills_thread():
    mock_thread.stop = Mock()
    m = Mock()
    socket.send_json = make_coroutine(m)
    pair_handler = pair_handling_factory(socket)

    await pair_handler(mock_thread, {'category': 'pairing', 'message': 'pair-start', 'data': {'pairing_id': "poop", "exit_flow": True}})

    mock_thread.stop.assert_called_once()