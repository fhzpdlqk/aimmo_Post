import jwt
from tests.factory.user_factory import UserFactory
from tests.factory.post_factory import PostFactory
from tests.factory.comment_factory import CommentFactory
from tests.factory.recomment_factory import ReCommentFactory
from app.config import TestConfig
from app.models import Post
import pytest


class Describe_MyPageView:
    class Test_My_Post:
        @pytest.fixture
        def posts(self, logged_in_user):
            return [PostFactory.create() for _ in range(10)] + [PostFactory.create(writer=logged_in_user) for _ in
                                                                range(20)]

        @pytest.fixture
        def trans_api(self, client, headers, posts):
            return client.get('/mypage/posts', headers=headers)

        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_post_목록_작성자_여부(self, trans_api, logged_in_user):
                post_list = trans_api.json
                assert len(post_list) == 20
                for post in post_list:
                    assert post["writer_email"] == logged_in_user.email

    class Test_My_Comment:
        @pytest.fixture
        def comments(self, logged_in_user):
            return [CommentFactory.create() for _ in range(10)] + [CommentFactory.create(writer=logged_in_user) for _ in range(20)]+ [ReCommentFactory.create(writer=logged_in_user) for _ in range(20)]

        @pytest.fixture
        def trans_api(self, client, headers, comments):
            return client.get('/mypage/comments', headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_댓글_목록_작성자_여부(self, trans_api, logged_in_user):
            comment_list = trans_api.json
            assert len(comment_list) == 20
            for comment in comment_list:
                assert comment["writer_email"] == logged_in_user.email

    class Test_My_ReComment:
        @pytest.fixture
        def comments(self, logged_in_user):
            return [CommentFactory.create() for _ in range(10)] + [CommentFactory.create(writer=logged_in_user) for _ in range(20)]+ [ReCommentFactory.create(writer=logged_in_user) for _ in range(20)]

        @pytest.fixture
        def trans_api(self, client, headers, comments):
            return client.get('/mypage/recomments', headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_댓글_목록_작성자_여부(self, trans_api, logged_in_user):
            recomment_list = trans_api.json
            assert len(recomment_list) == 20
            for recomment in recomment_list:
                assert recomment["writer_email"] == logged_in_user.email

    class Test_My_Like:
        @pytest.fixture
        def posts(self, logged_in_user):
            return [PostFactory.create() for _ in range(10)] + [PostFactory.create(like=[logged_in_user]) for _ in
                                                                range(20)]

        @pytest.fixture
        def trans_api(self, client, headers, posts):
            return client.get('/mypage/likes', headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_게시글_목록_좋아요_여부(self, trans_api, logged_in_user):
            post_list = trans_api.json
            assert len(post_list) == 20
            for post in post_list:
                assert logged_in_user in Post.objects(id=post["id"]).get().like
