import pytest
import jwt
from tests.factory.user_factory import UserFactory
from tests.factory.board_factory import BoardFactory
from tests.factory.post_factory import PostFactory
from tests.factory.comment_factory import CommentFactory
from app.config import TestConfig

@pytest.fixture
def headers(token):
    return {
        "Authorization": token,
        'Content-Type': 'application/json'
    }


@pytest.fixture
def logged_in_user():
    return UserFactory.create()

@pytest.fixture
def token(logged_in_user):
    return jwt.encode({"email": logged_in_user["email"], "is_master": logged_in_user["is_master"]},
                        TestConfig.TOKEN_KEY, TestConfig.ALGORITHM)

@pytest.fixture
def board():
    return BoardFactory.create()

@pytest.fixture
def post(board, logged_in_user):
    return PostFactory.create(board=board, writer=logged_in_user.email)

@pytest.fixture
def comment(post, logged_in_user):
    return CommentFactory.create(post=post.id, writer=logged_in_user.email)