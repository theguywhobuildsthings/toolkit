from backend.models import schemas
from backend.tests.integration.client import client
from backend.models.user.user_repository import UserRepository
from backend.tests.data.data_factory import UserFactory
from backend.tests.utils.session import log_in

repo = UserRepository()


def test_valid_user_is_created():
    res = client.post("/user", json={"username": "test_user", "password": "test_pass"})
    assert res.status_code == 200, "Expected a successful response"
    assert (
        repo.get_user_by_username("test_user") is not None
    ), "Expected user to be created"


def test_invalid_user_is_not_created():
    res = client.post("/user", json={"username": "test user", "password": "test_pass"})
    assert res.status_code == 400, "Expected rejection"
    assert (
        repo.get_user_by_username("test user") is None
    ), "Expected user not to be created"


def test_logged_out_user_not_given_info():
    res = client.get("/user")
    assert (
        res.status_code == 401
    ), "Expected missing validation headers to prevent access"


def test_logged_in_user_given_info():
    access_token = log_in()

    res = client.get("/user", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200, "Expected logged in user to get information"
