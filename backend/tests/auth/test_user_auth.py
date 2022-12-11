
import pytest
import logging

from backend.auth.user_auth import UserAuth
from unittest.mock import MagicMock
from backend.models import db
from backend.models.user.user_repository import UserRepository
from backend.tests.data import test_users

logger = logging.getLogger('output')

user_auth: UserAuth = None
mock_user_repo: UserRepository = None
fake_username = "FakeUser"

# def test_correct_password():
#     mock_user_repo = UserRepository()
#     mock_user_repo.get_user_by_username = MagicMock(return_value=test_users.db_user_1)
#     user_auth = UserAuth(fake_username, test_users.db_user_1_pass, mock_user_repo)
#     user = user_auth.get_authenticated_user()
    
#     assert user.id == 54, "Should verify user succesfully"
    
#     user_auth = None
#     mock_user_repo = None

# def test_incorrect_password():
#     mock_user_repo = UserRepository()
#     mock_user_repo.get_user_by_username = MagicMock(return_value=test_users.db_user_1)
#     user_auth = UserAuth(fake_username, "not_the_password", mock_user_repo)
#     user = user_auth.get_authenticated_user()
    
#     assert user == None, "Should verify user succesfully"
    
#     user_auth = None
#     mock_user_repo = None