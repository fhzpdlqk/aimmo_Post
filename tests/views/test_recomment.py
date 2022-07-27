import pytest
import jwt
from json import dumps
from app.models import Comment, ReComment
from tests.factory.comment_factory import CommentFactory
from tests.factory.recomment_factory import ReCommentFactory


class Describe_ReCommentView:

    @pytest.fixture
    def recomment(self, comment, logged_in_user):
        return ReCommentFactory.create(comment=comment, writer=logged_in_user.user_id)

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

        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_삽입여부(self, trans_api, form, comment):
                assert len(ReComment.objects()) == 1
                assert Comment.objects(id=comment.id).get().num_recomment == comment.num_recomment + 1

            def test_데이터_확인(self, trans_api, form, logged_in_user, comment):
                assert ReComment.objects()[0].content == form["content"]
                assert ReComment.objects()[0].writer == logged_in_user.user_id
                assert ReComment.objects()[0].comment == Comment.objects(id=comment.id).get()

    class Test_Update_ReComment:
        @pytest.fixture
        def form(self):
            return {
                "content": "make_recomment_test_update"
            }

        @pytest.fixture
        def trans_api(self, form, client, headers, board, post, comment, recomment):
            return client.put(
                f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/recomments/{str(recomment.id)}',
                data=dumps(form),
                headers=headers)
        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, form, logged_in_user, comment):
                assert ReComment.objects()[0].content == form["content"]
                assert ReComment.objects()[0].writer == logged_in_user.user_id
                assert ReComment.objects()[0].comment == Comment.objects(id=comment.id).get()

    class Test_Delete_ReComment:
        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment, recomment):
            return client.delete(
                f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/recomments/{str(recomment.id)}',
                headers=headers)

        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_개수_확인(self, trans_api, comment):
                assert ReComment.objects(comment=comment.id, is_deleted=False).count() == 0
                assert Comment.objects(id=comment.id).get().num_recomment == comment.num_recomment-1

    class Test_Like_ReComment:
        @pytest.fixture
        def recomment(self, comment, logged_in_user):
            return ReCommentFactory.create(comment=comment.id, writer=logged_in_user.user_id)

        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment, recomment):
            return client.post(
                f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/recomments/{str(recomment.id)}/like',
                headers=headers)
        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, logged_in_user, recomment):
                assert logged_in_user in ReComment.objects(id=recomment.id).get().like

        class Context_이미_좋아요가_눌러져_있을_경우:
            @pytest.fixture
            def recomment(self, logged_in_user, board, comment):
                return ReCommentFactory.create(comment=comment.id, writer=logged_in_user.user_id, like=[logged_in_user])

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 400

            def test_데이터_확인(self, trans_api, post, logged_in_user, comment, recomment):
                assert logged_in_user in ReComment.objects(id=recomment.id).get().like


    class Test_UnLike_ReComment:
        @pytest.fixture
        def recomment(self, comment, logged_in_user):
            return ReCommentFactory.create(comment=comment.id, writer=logged_in_user.user_id, like=[logged_in_user])

        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment, recomment):
            return client.post(
                f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/recomments/{str(recomment.id)}/like_cancel',
                headers=headers)
        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, logged_in_user, recomment):
                assert logged_in_user not in ReComment.objects(id=recomment.id).get().like

        class Context_이미_좋아요가_눌러져_있을_경우:
            @pytest.fixture
            def recomment(self, logged_in_user, board, comment):
                return ReCommentFactory.create(comment=comment.id, writer=logged_in_user.user_id, like=[])

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 400

            def test_데이터_확인(self, trans_api, post, logged_in_user, comment, recomment):
                assert logged_in_user not in ReComment.objects(id=recomment.id).get().like
