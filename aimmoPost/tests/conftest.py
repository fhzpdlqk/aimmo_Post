import pytest
import aimmoPost.aimmoPost as ai
import mongoengine as me
from flask import current_app
import jwt
from aimmoPost.tests.factory.post_factory import PostFactory
from aimmoPost.tests.factory.comment_factory import CommentFactory


@pytest.fixture(scope="session", autouse=True)
def app():
    return ai.app.test_client()


@pytest.fixture(scope="function", autouse=True)
def db(app):
    app.application.config["DATABASE"] = "mongomock://localhost"
    db = me.connect("test", host="mongomock://localhost", alias="test")
    yield db
    db.drop_database("test")
    db.close()


@pytest.fixture(scope="function")
def id_token():
    return jwt.encode({"user_id": "testid"}, "abcd", algorithm="HS256")


@pytest.fixture
def post():
    return PostFactory.create()


@pytest.fixture
def comment():
    return CommentFactory.create()
