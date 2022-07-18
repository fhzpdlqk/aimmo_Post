import pytest
import jwt
from json import dumps
from app.models import Post, Comment
from app.config import TestConfig
from tests.factory.user_factory import UserFactory
from tests.factory.board_factory import BoardFactory
from tests.factory.post_factory import PostFactory
from tests.factory.comment_factory import CommentFactory


class TestCommentView:
    @pytest.fixture
    def login_user(self):
        return UserFactory.create()

    @pytest.fixture
    def token(self, login_user):
        return jwt.encode({"user_id": login_user["user_id"], "is_master": login_user["is_master"]},
                          TestConfig.TOKEN_KEY, TestConfig.ALGORITHM)

    @pytest.fixture
    def board(self):
        return BoardFactory.create()

    @pytest.fixture
    def post(self, board, login_user):
        post = PostFactory.create(board=board.id, writer=login_user.user_id)
        return post

    class Test_Make_Comment:
        @pytest.fixture
        def form(self):
            return {
                "content": "make_comment_test"
            }

        @pytest.fixture
        def trans_api(self, form, client, headers, board, post):
            return client.post(f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/', data=dumps(form),
                               headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_삽입여부(self, trans_api, form, post):
            assert len(Comment.objects()) == 1
            assert Post.objects(id=post.id).get().num_comment == 1

        def test_데이터_확인(self, trans_api, form, login_user, post):
            assert Comment.objects()[0].content == form["content"]
            assert Comment.objects()[0].writer == login_user.user_id
            assert Comment.objects()[0].post == Post.objects(id=post.id).get()

    class Test_Update_Comment:
        @pytest.fixture
        def form(self):
            return {
                "content": "update_comment_content"
            }

        @pytest.fixture
        def comment(self, post, login_user):
            return CommentFactory.create(post=post.id, writer=login_user.user_id)

        @pytest.fixture
        def trans_api(self, form, client, headers, board, post, comment):
            return client.put(f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}',
                              data=dumps(form), headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api, form, post, comment, login_user):
            assert Comment.objects(id=comment.id).get().content == form["content"]
            assert Comment.objects(id=comment.id).get().writer == login_user.user_id
            assert Comment.objects(id=comment.id).get().post == post

    class Test_Delete_Comment:
        @pytest.fixture
        def post(self, board, login_user):
            post = PostFactory.create(board=board.id, writer=login_user.user_id, num_comment=1)
            return post

        @pytest.fixture
        def comment(self, post, login_user):
            return CommentFactory.create(post=post.id, writer=login_user.user_id)

        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment):
            return client.delete(f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}',
                                 headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터개수_확인(self, trans_api, post, comment, login_user):
            assert Comment.objects(post=post.id, is_deleted=False).count() == 0
            assert Post.objects(id=post.id).get().num_comment == 0

    class Test_Like_Comment:
        @pytest.fixture
        def comment(self, post, login_user):
            return CommentFactory.create(post=post.id, writer=login_user.user_id)

        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment):
            return client.post(f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/like',
                               headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api, post, login_user, comment):
            assert login_user in Comment.objects(id=comment.id).get().like

        class Test_이미_좋아요가_눌러져_있을_경우:
            @pytest.fixture
            def comment(self, login_user, board, post):
                return CommentFactory.create(post=post.id, writer=login_user.user_id, like=[login_user])

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post, login_user, comment):
                assert login_user not in Comment.objects(id=comment.id).get().like
