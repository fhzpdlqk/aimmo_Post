import jwt
from tests.factory.user_factory import UserFactory
from tests.factory.post_factory import PostFactory
from tests.factory.comment_factory import CommentFactory
from app.config import TestConfig
from app.models import Post
import pytest

class Test_MyPageView:
    @pytest.fixture
    def login_user(self):
        return UserFactory.create()

    @pytest.fixture
    def token(self, login_user):
        return jwt.encode({"user_id": login_user["user_id"], "is_master": login_user["is_master"]},
                          TestConfig.TOKEN_KEY, TestConfig.ALGORITHM)

    class Test_My_Post:
        @pytest.fixture
        def posts(self, login_user):
            return [PostFactory.create() for _ in range(10)] + [PostFactory.create(writer=login_user.user_id) for _ in range(20)]
        @pytest.fixture
        def trans_api(self, client, headers, posts):
            return client.get('/mypage/posts', headers=headers)

        def test_상태코드_200(self,trans_api):
            assert trans_api.status_code == 200

        def test_post_목록_작성자_여부(self, trans_api, login_user):
            post_list = trans_api.json
            assert len(post_list) == 20
            for post in post_list:
                assert post["writer"] == login_user.user_id


    class Test_My_Comment:
        @pytest.fixture
        def posts(self, login_user):
            return [CommentFactory.create() for _ in range(10)] + [CommentFactory.create(writer=login_user.user_id) for _ in range(20)]
        @pytest.fixture
        def trans_api(self, client, headers, posts):
            return client.get('/mypage/comments', headers=headers)

        def test_상태코드_200(self,trans_api):
            assert trans_api.status_code == 200

        def test_댓글_목록_작성자_여부(self, trans_api, login_user):
            comment_list = trans_api.json["comments"]
            assert len(comment_list) == 20
            for post in comment_list:
                assert post["writer"] == login_user.user_id

    class Test_My_Like:
        @pytest.fixture
        def posts(self, login_user):
            return [PostFactory.create() for _ in range(10)] + [PostFactory.create(like=[login_user]) for _ in range(20)]
        @pytest.fixture
        def trans_api(self, client, headers, posts):
            return client.get('/mypage/likes', headers=headers)

        def test_상태코드_200(self,trans_api):
            assert trans_api.status_code == 200

        def test_게시글_목록_좋아요_여부(self, trans_api, login_user):
            post_list = trans_api.json
            assert len(post_list) == 20
            for post in post_list:
                assert login_user in Post.objects(id=post["id"]).get().like
