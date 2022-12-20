from unittest import TestCase
from unittest.mock import MagicMock, Mock
import uuid

import pytest
from backend.models import schemas
from backend.models.pair.pair_repository import PairRepository
from backend.pair.pair_utils import handle_ws_request
from backend.tests.data.test_users import schema_user_1

pair_repo = PairRepository()


@pytest.mark.asyncio
async def test_empty_data_is_ignored():
    pair_repo.create_pair = Mock()
    await handle_ws_request({}, uuid.uuid4(), schema_user_1, pair_repo)
    pair_repo.create_pair.assert_not_called()


@pytest.mark.asyncio
async def test_data_type_that_isnt_request_is_ignored():
    pair_repo.create_pair = Mock()
    await handle_ws_request(
        {"type": "request1"}, uuid.uuid4(), schema_user_1, pair_repo
    )
    pair_repo.create_pair.assert_not_called()


@pytest.mark.asyncio
async def test_request_without_data_is_ignored():
    pair_repo.create_pair = Mock()
    await handle_ws_request({"type": "request"}, uuid.uuid4(), schema_user_1, pair_repo)
    pair_repo.create_pair.assert_not_called()


@pytest.mark.asyncio
async def test_request_with_empty_data_is_ignored():
    pair_repo.create_pair = Mock()
    await handle_ws_request(
        {"type": "request", "request": {}}, uuid.uuid4(), schema_user_1, pair_repo
    )
    pair_repo.create_pair.assert_not_called()


@pytest.mark.asyncio
async def test_request_with_invalid_type_is_ignored():
    pair_repo.create_pair = Mock()
    await handle_ws_request(
        {"type": "request", "request": {"type": "test"}},
        uuid.uuid4(),
        schema_user_1,
        pair_repo,
    )
    pair_repo.create_pair.assert_not_called()


@pytest.mark.asyncio
async def test_valid_request_creates_pair():
    pair_repo.create_pair = Mock()
    in_uuid = uuid.uuid4()
    await handle_ws_request(
        {"type": "request", "request": {"type": "pair-data"}},
        in_uuid,
        schema_user_1,
        pair_repo,
    )
    pair_repo.create_pair.assert_called_once_with(
        schema_user_1, schemas.Pair(uuid=str(in_uuid), pair_status="unpaired")
    )


@pytest.mark.asyncio
async def test_valid_request_returns_message():
    pair_repo.create_pair = Mock()
    in_uuid = uuid.uuid4()
    output = await handle_ws_request(
        {"type": "request", "request": {"type": "pair-data"}},
        in_uuid,
        schema_user_1,
        pair_repo,
    )
    expected_output = {
        "message": "pair-info",
        "data": {"uuid": str(in_uuid), "pair_url_path": f"/pair/start/{str(in_uuid)}"},
    }
    TestCase().assertDictEqual(expected_output, output)
