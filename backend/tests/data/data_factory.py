import factory
from backend.models import db
from backend.db import database


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = db.User
        # django_get_or_create = ('username',)
        sqlalchemy_session = database.SessionLocal()

    username = "test_user"
    # 'test_pass'
    password = "$2a$12$FeUFarQa1wFl7h3uH8Cbqe0aUXI5yOXeV2I8bVOK8XOTV..hiinmC"
    pairs = []
