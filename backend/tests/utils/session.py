from backend.auth.serve import create_access_token
from backend.tests.data.data_factory import UserFactory


def log_in() -> str:
    user = UserFactory.create()
    access_token = create_access_token(data={"sub": user.username})
    return access_token
