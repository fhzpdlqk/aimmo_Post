import pytest
from json import dumps
from app.models import Post, Comment
from tests.factory.comment_factory import CommentFactory


class Describe_CommentView:

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

        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_삽입여부(self, trans_api, form, post):
                assert len(Comment.objects()) == 1
                assert Post.objects(id=post.id).get().num_comment == post.num_comment+1

            def test_데이터_확인(self, trans_api, form, logged_in_user, post):
                assert Comment.objects()[0].content == form["content"]
                assert Comment.objects()[0].writer.email == logged_in_user.email
                assert Comment.objects()[0].post == Post.objects(id=post.id).get()

    class Test_Update_Comment:
        @pytest.fixture
        def form(self):
            return {
                "content": "update_comment_content"
            }

        @pytest.fixture
        def trans_api(self, form, client, headers, board, post, comment):
            return client.put(f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}',
                              data=dumps(form), headers=headers)
        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, form, post, comment, logged_in_user):
                assert Comment.objects(id=comment.id).get().content == form["content"]
                assert Comment.objects(id=comment.id).get().writer.email == logged_in_user.email
                assert Comment.objects(id=comment.id).get().post == post

    class Test_Delete_Comment:
        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment):
            return client.delete(f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}',
                                 headers=headers)

        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터개수_확인(self, trans_api, post, comment):
                assert Comment.objects(post=post.id, is_deleted=False).count() == 0
                assert Post.objects(id=post.id).get().num_comment == post.num_comment-1

    class Test_Like_Comment:
        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment):
            return client.post(f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/like',
                               headers=headers)

        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post, logged_in_user, comment):
                assert logged_in_user in Comment.objects(id=comment.id).get().like

        class Context_이미_좋아요가_눌러져_있을_경우:
            @pytest.fixture
            def comment(self, logged_in_user, board, post):
                return CommentFactory.create(post=post.id, writer=logged_in_user.email, like=[logged_in_user])

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 400

            def test_데이터_확인(self, trans_api, post, logged_in_user, comment):
                assert logged_in_user in Comment.objects(id=comment.id).get().like

    class Test_UnLike_Comment:
        @pytest.fixture
        def comment(self, post, logged_in_user):
            return CommentFactory.create(post=post.id, writer=logged_in_user.email, like=[logged_in_user])

        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment):
            return client.post(f'/boards/{str(board.id)}/posts/{str(post.id)}/comments/{str(comment.id)}/like_cancel',
                               headers=headers)
        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post, logged_in_user, comment):
                assert logged_in_user not in Comment.objects(id=comment.id).get().like

        class Context_좋아요가_눌러져_있지_않은_경우:
            @pytest.fixture
            def comment(self, logged_in_user, board, post):
                return CommentFactory.create(post=post.id, writer=logged_in_user.email, like=[])

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 400

            def test_데이터_확인(self, trans_api, post, logged_in_user, comment):
                assert logged_in_user not in Comment.objects(id=comment.id).get().like
