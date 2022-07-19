import pytest
import jwt
from json import dumps
from app.models import Comment, ReComment
from app.config import TestConfig
from tests.factory.user_factory import UserFactory
from tests.factory.board_factory import BoardFactory
from tests.factory.post_factory import PostFactory
from tests.factory.comment_factory import CommentFactory
from tests.factory.recomment_factory import ReCommentFactory


class TestReCommentView:
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

    @pytest.fixture
    def comment(self, post, login_user):
        return CommentFactory.create(post=post.id, writer=login_user.user_id)

    class Test_Make_ReComment:
        @pytest.fixture
        def form(self):
            return {
                "content": "make_recomment_test"
            }

        @pytest.fixture
        def trans_api(self, form, client, headers, board, post, comment):
            return client.post(f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/recomments/',
                               data=dumps(form),
                               headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_삽입여부(self, trans_api, form, comment):
            assert len(ReComment.objects()) == 1
            assert Comment.objects(id=comment.id).get().num_recomment == 1

        def test_데이터_확인(self, trans_api, form, login_user, comment):
            assert ReComment.objects()[0].content == form["content"]
            assert ReComment.objects()[0].writer == login_user.user_id
            assert ReComment.objects()[0].comment == Comment.objects(id=comment.id).get()

    class Test_Update_ReComment:
        @pytest.fixture
        def form(self):
            return {
                "content": "make_recomment_test_update"
            }

        @pytest.fixture
        def recomment(self, comment, login_user):
            return ReCommentFactory.create(comment=comment, writer=login_user.user_id)

        @pytest.fixture
        def trans_api(self, form, client, headers, board, post, comment, recomment):
            return client.put(
                f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/recomments/{str(recomment.id)}',
                data=dumps(form),
                headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api, form, login_user, comment):
            assert ReComment.objects()[0].content == form["content"]
            assert ReComment.objects()[0].writer == login_user.user_id
            assert ReComment.objects()[0].comment == Comment.objects(id=comment.id).get()

    class Test_Delete_ReComment:
        @pytest.fixture
        def comment(self, post, login_user):
            return CommentFactory.create(num_recomment=1, post=post, writer=login_user.user_id)

        @pytest.fixture
        def recomment(self, comment, login_user):
            return ReCommentFactory.create(comment=comment, writer=login_user.user_id)

        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment, recomment):
            return client.delete(
                f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/recomments/{str(recomment.id)}',
                headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_개수_확인(self, trans_api, login_user, comment):
            assert ReComment.objects(comment=comment.id, is_deleted=False).count() == 0
            assert Comment.objects(id=comment.id).get().num_recomment == 0

    class Test_Like_ReComment:
        @pytest.fixture
        def recomment(self, comment, login_user):
            return ReCommentFactory.create(comment=comment.id, writer=login_user.user_id)

        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment, recomment):
            return client.post(
                f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/recomments/{str(recomment.id)}/like',
                headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api, post, login_user, recomment):
            assert login_user in ReComment.objects(id=recomment.id).get().like

        class Test_이미_좋아요가_눌러져_있을_경우:
            @pytest.fixture
            def recomment(self, login_user, board, comment):
                return ReCommentFactory.create(comment=comment.id, writer=login_user.user_id, like=[login_user])

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 400

            def test_데이터_확인(self, trans_api, post, login_user, comment, recomment):
                assert login_user in ReComment.objects(id=recomment.id).get().like


    class Test_UnLike_ReComment:
        @pytest.fixture
        def recomment(self, comment, login_user):
            return ReCommentFactory.create(comment=comment.id, writer=login_user.user_id, like=[login_user])

        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment, recomment):
            return client.post(
                f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/recomments/{str(recomment.id)}/like_cancel',
                headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api, post, login_user, recomment):
            assert login_user not in ReComment.objects(id=recomment.id).get().like

        class Test_이미_좋아요가_눌러져_있을_경우:
            @pytest.fixture
            def recomment(self, login_user, board, comment):
                return ReCommentFactory.create(comment=comment.id, writer=login_user.user_id, like=[])

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 400

            def test_데이터_확인(self, trans_api, post, login_user, comment, recomment):
                assert login_user not in ReComment.objects(id=recomment.id).get().like
