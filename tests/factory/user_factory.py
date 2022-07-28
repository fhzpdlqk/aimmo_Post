import factory
from factory.mongoengine import MongoEngineFactory
from app.models import User
from factory import fuzzy
import bcrypt


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    password = bcrypt.hashpw("test_user_pw".encode("utf-8"), bcrypt.gensalt())
    is_master = False
