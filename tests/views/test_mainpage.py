from json import dumps
import pytest
import random
import jwt
from app.config import TestConfig
from tests.factory.post_factory import PostFactory
from tests.factory.user_factory import UserFactory


class Describe_MainPageView:
    @pytest.fixture
    def login_user(self):
        return UserFactory.create()

    @pytest.fixture
    def token(self, login_user):
        return jwt.encode({"user_id": login_user["user_id"], "is_master": login_user["is_master"]},
                          TestConfig.TOKEN_KEY, TestConfig.ALGORITHM)

    @pytest.fixture
    def post(self):
        PostFactory.create(num_comment=random.randint(1, 10),
                           like=[UserFactory.create() for _ in range(random.randint(1, 10))])

    class Test_Mainpage:
        class Context_최신순_게시물:
            @pytest.fixture
            def trans_api(self, client, post, headers):
                return client.get('/?filter=date', headers=headers)

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_목록_최신순_여부(self, trans_api):
                post_list = trans_api.json
                for index in range(1, len(post_list)):
                    assert post_list[index - 1]["date"] >= post_list[index]["date"]
        class Context_댓글순_게시물:
            @pytest.fixture
            def trans_api(self, client, post, headers):
                return client.get('/?filter=comment', headers=headers)

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_목록_댓글순_여부(self, trans_api):
                post_list = trans_api.json
                for index in range(1, len(post_list)):
                    assert post_list[index - 1]["num_comment"] >= post_list[index]["num_comment"]

        class Context_like_List:
            @pytest.fixture
            def trans_api(self, client, post, headers):
                return client.get('/?filter=like', headers=headers)

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_목록_좋아요순_여부(self, trans_api):
                post_list = trans_api.json
                for index in range(1, len(post_list)):
                    assert post_list[index - 1]["num_like"] >= post_list[index]["num_like"]
