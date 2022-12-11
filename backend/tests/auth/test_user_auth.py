
import pytest
import logging

from backend.auth.user_auth import UserAuth
from unittest.mock import MagicMock
from backend.models import db
from backend.models.user.user_repository import UserRepository

logger = logging.getLogger('output')


unhashed_correct_password = "test_pass"
unhashed_incorrect_password = "test_pass1"
hash_password = "$2a$16$4.y0.knaCcFB8B6l5.haSujcFI78Wv1ue442FsVvezunBaREv.i7e"
user_auth: UserAuth = None
mock_user_repo: UserRepository = None
fake_username = "FakeUser"
fake_db_user = db.User(id=54, username=fake_username, password=hash_password, pairs=[])


def test_correct_password():
    mock_user_repo = UserRepository()
    mock_user_repo.get_user_by_username = MagicMock(return_value=fake_db_user)
    user_auth = UserAuth(fake_username, unhashed_correct_password, mock_user_repo)
    user = user_auth.get_authenticated_user()
    
    assert user.id == 54, "Should verify user succesfully"
    
    user_auth = None
    mock_user_repo = None

def test_incorrect_password():
    mock_user_repo = UserRepository()
    mock_user_repo.get_user_by_username = MagicMock(return_value=fake_db_user)
    user_auth = UserAuth(fake_username, unhashed_incorrect_password, mock_user_repo)
    user = user_auth.get_authenticated_user()
    
    assert user == None, "Should verify user succesfully"
    
    user_auth = None
    mock_user_repo = None