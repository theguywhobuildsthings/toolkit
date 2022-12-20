from unittest.mock import MagicMock
from fastapi import HTTPException
import pytest

from backend.auth import serve
from jose import jwt
import datetime

from backend.models.user.user_repository import UserRepository
from backend.tests.data import test_users


def test_token_encoding():
    data = {"test_fake_data": "test test"}
    encoded = serve.create_access_token(data)
    unencoded = jwt.decode(encoded, serve.SECRET_KEY, algorithms=[serve.ALGORITHM])
    assert (
        unencoded["test_fake_data"] == "test test"
    ), "Data should encode without changing"


def test_token_expiring():
    data = {"test_fake_data": "test test"}
    time_delta = datetime.timedelta(minutes=15)
    date_encoded = datetime.datetime.now()
    encoded = serve.create_access_token(data, expires_delta=time_delta)
    unencoded = jwt.decode(encoded, serve.SECRET_KEY, algorithms=[serve.ALGORITHM])
    expected_time = date_encoded + time_delta
    assert unencoded["exp"] == int(
        expected_time.timestamp()
    ), "Token should have a valid expiry"


@pytest.mark.asyncio
async def test_success_verify_token():
    mock_user_repo = UserRepository()
    mock_user_repo.get_user_by_username = MagicMock(return_value=test_users.db_user_1)

    data = {"sub": test_users.db_user_1.username}
    encoded = serve.create_access_token(data)

    verified_user = await serve.get_current_user(encoded, mock_user_repo)

    assert verified_user == test_users.db_user_1, "Should verify token as valid"


@pytest.mark.asyncio
async def test_verify_unsuccessful_token():
    with pytest.raises(HTTPException) as e:
        mock_user_repo = UserRepository()
        mock_user_repo.get_user_by_username = MagicMock(return_value=None)

        data = {"sub": test_users.db_user_1.username}
        encoded = serve.create_access_token(data)

        await serve.get_current_user(encoded, mock_user_repo)

    assert e.value.status_code == 401, "Should raise 401 exception for client"


@pytest.mark.asyncio
async def test_verify_invalid_token():
    with pytest.raises(HTTPException) as e:
        mock_user_repo = UserRepository()
        mock_user_repo.get_user_by_username = MagicMock(
            return_value=test_users.db_user_1
        )

        data = {"sub": test_users.db_user_1.username}
        encoded = serve.create_access_token(data, key="fake_secret")

        await serve.get_current_user(encoded, repo=mock_user_repo)

    assert e.value.status_code == 401, "Should raise 401 exception for client"
