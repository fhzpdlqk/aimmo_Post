import factory
from factory.mongoengine import MongoEngineFactory
from aimmoPost.aimmoPost.models.User import User
import datetime
import bcrypt


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    user_id = "testid"
    salt = bcrypt.gensalt()
    user_pw = bcrypt.hashpw("testpw".encode("utf-8"), salt)
