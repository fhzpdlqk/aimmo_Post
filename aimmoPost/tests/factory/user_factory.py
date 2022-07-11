import factory
from factory.mongoengine import MongoEngineFactory
from app.models import User
import bcrypt


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    user_id = "test_user_id"
    user_pw = bcrypt.hashpw("test_user_pw".encode("utf-8"), bcrypt.gensalt())
    is_master = False
