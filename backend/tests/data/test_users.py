from backend.models import db, schemas

db_user_1 = db.User(
    id=54,
    username="FakeUser",
    password="$2a$16$4.y0.knaCcFB8B6l5.haSujcFI78Wv1ue442FsVvezunBaREv.i7e",
    pairs=[],
)
db_user_1_pass = "test_pass"

schema_user_1 = schemas.User(id=54, username="FakeUser", pairs=[])
