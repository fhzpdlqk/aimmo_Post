from factory.mongoengine import MongoEngineFactory
from app.models import User
from faker import Faker
import bcrypt


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    email = Faker().email()
    password = bcrypt.hashpw("test_user_pw".encode("utf-8"), bcrypt.gensalt())
    is_master = False
