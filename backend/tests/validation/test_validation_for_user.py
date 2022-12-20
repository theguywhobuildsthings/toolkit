import json
import pytest
from backend.models import db

user_object: db.User = db.User()


def test_username_has_no_spaces():
    with pytest.raises(ValueError) as e:
        user_object.validate_username(key="username", value="bad username")
    assert (
        e.value.args[0] == "Username should not contain spaces"
    ), "Expected to get the correct validation exception"


def test_valid_usernames():
    user_object.validate_username(key="username", value="good_username")
    user_object.validate_username(key="username", value="goodusername")
    user_object.validate_username(key="username", value="good.username")
    user_object.validate_username(
        key="username", value="12345678901234567890123456789012345678901234567890"
    )


def test_username_too_long():
    with pytest.raises(ValueError) as e:
        user_object.validate_username(
            key="username",
            value="bad_username_because_it_is_way_longer_than_we_would_ever_expect_a_username_to_be.we_dont_need_to_take_up_much_space_for_these",
        )
    assert (
        e.value.args[0] == "Username should not be longer than 50 chars"
    ), "Expected to get the correct validation exception"


# test_
