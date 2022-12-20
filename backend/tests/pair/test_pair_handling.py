from unittest.mock import Mock
import pytest
import websockets
from backend.models.pair.pair_repository import PairRepository
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
    await pair_handler(mock_thread, {"bad": "data"})
    # Has correct category and message but doesn't carry data
    await pair_handler(mock_thread, {"category": "pairing", "message": "pair-start"})
    # Has correct category and message but doesn't carry data
    await pair_handler(
        mock_thread,
        {"category": "pairing", "message": "pair-start", "data": {"bad": "data"}},
    )
    # Has correct data and category with no message
    await pair_handler(
        mock_thread, {"category": "pairing", "data": {"pair_id": "poop"}}
    )

    m.assert_not_called()


@pytest.mark.asyncio
async def test_valid_confirm_calls_websocket():
    m = Mock()
    socket.send_json = make_coroutine(m)
    pair_handler = pair_handling_factory(socket)

    mock_pair_repo = PairRepository()
    mock_pair_repo.update_pair_status = Mock(return_value=True)

    await pair_handler(
        mock_thread,
        {"category": "pairing", "message": "pair-confirm", "data": {"pair_id": "poop"}},
        mock_pair_repo,
    )

    m.assert_called_once_with({"message": "pair-complete", "pair_id": "poop"})


@pytest.mark.asyncio
async def test_valid_start_calls_websocket():
    m = Mock()
    socket.send_json = make_coroutine(m)
    pair_handler = pair_handling_factory(socket)
    mock_pair_repo = PairRepository()
    mock_pair_repo.update_pair_status = Mock(return_value=True)
    await pair_handler(
        mock_thread,
        {"category": "pairing", "message": "pair-start", "data": {"pair_id": "poop"}},
        mock_pair_repo,
    )

    m.assert_called_once_with({"message": "pair-start", "pair_id": "poop"})


@pytest.mark.asyncio
async def test_invalid_start_fails():
    m = Mock()
    socket.send_json = make_coroutine(m)
    pair_handler = pair_handling_factory(socket)
    mock_pair_repo = PairRepository()
    mock_pair_repo.update_pair_status = Mock(return_value=False)
    await pair_handler(
        mock_thread,
        {"category": "pairing", "message": "pair-start", "data": {"pair_id": "poop"}},
        mock_pair_repo,
    )

    m.assert_called_once_with({"message": "pair-fail", "pair_id": "poop"})


@pytest.mark.asyncio
async def test_valid_exit_kills_thread():
    mock_thread.stop = Mock()
    m = Mock()
    socket.send_json = make_coroutine(m)
    pair_handler = pair_handling_factory(socket)

    await pair_handler(
        mock_thread,
        {
            "category": "pairing",
            "message": "pair-complete",
            "data": {"pair_id": "poop", "exit_flow": True},
        },
    )

    mock_thread.stop.assert_called_once()
