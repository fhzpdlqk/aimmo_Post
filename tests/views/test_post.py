import pytest
import random
from json import dumps
from app.models import Post
from tests.factory.post_factory import PostFactory
from tests.factory.comment_factory import CommentFactory


class Describe_PostView:

    class Test_Make_Post:

        @pytest.fixture
        def form(self):
            return {
                "title": "make_post_title",
                "content": "make_post_content",
                "tag": ["make_tag_1", "make_tag_2"],
                "notice": True
            }

        @pytest.fixture
        def trans_api(self, form, client, headers, board):
            return client.post(f'/boards/{str(board.id)}/posts/', data=dumps(form), headers=headers)

        class Context_정상_요청:
            def test_상태코드_201(self, trans_api):
                assert trans_api.status_code == 201

            def test_데이터_삽입여부(self, trans_api, form):
                assert len(Post.objects()) == 1

            def test_데이터_확인(self, trans_api, form):
                assert Post.objects()[0].title == form["title"]
                assert Post.objects()[0].content == form["content"]
                assert Post.objects()[0].tag == form["tag"]
                assert Post.objects()[0].notice == form["notice"]
                assert not Post.objects()[0].is_deleted


    class Test_Get_Post:
        @pytest.fixture
        def trans_api(self, client, headers, board, post, comment):
            return client.get(f'/boards/{str(board.id)}/posts/{str(post.id)}', headers=headers)

        @pytest.fixture
        def comment(self, post):
            return [CommentFactory.create(post=post) for _ in range(post.num_comment)]

        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post):
                assert str(post.id) == trans_api.json["id"]
                assert post.title == trans_api.json["title"]
                assert post.content == trans_api.json["content"]
                assert post.writer.email == trans_api.json["writer_email"]
                assert post.notice == trans_api.json["notice"]
                assert len(post.like) == trans_api.json["num_like"]
                assert post.tag == trans_api.json["tag"]
                assert post.date.isoformat(timespec='microseconds') == trans_api.json["date"]
                assert post.num_comment == trans_api.json["num_comment"]
                assert len(trans_api.json["comment"]) == post.num_comment
                assert not post.is_deleted
        class Context_게시물이_삭제된_게시물일_경우:
            @pytest.fixture
            def post(self, board, logged_in_user):
                return PostFactory.create(board=board, writer=logged_in_user.email, is_deleted=True)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

    class Test_Delete_Post:
        @pytest.fixture
        def trans_api(self, client, board, headers, post):
            return client.delete(f"/boards/{str(board.id)}/posts/{str(post.id)}", headers=headers)

        class Context_정상_요청:
            def test_상태코드_204(self, trans_api):
                assert trans_api.status_code == 204

            def test_삭제_여부(self, post, trans_api):
                assert Post.objects(id=post.id).get().is_deleted

    class Test_Update_Post:
        @pytest.fixture
        def form(self):
            return {
                "title": "update_post_title",
                "content": "update_post_content",
                "tag": ["update_tag_1", "update_tag_2"],
                "notice": True
            }

        @pytest.fixture
        def trans_api(self, form, client, headers, board, post):
            return client.put(f'/boards/{str(board.id)}/posts/{str(post.id)}', data=dumps(form), headers=headers)

        class Context_정상_요청:
            def test_상태코드_201(self, trans_api):
                assert trans_api.status_code == 201

            def test_데이터_확인(self, trans_api, form, post):
                assert Post.objects(id=post.id).get().title == form["title"]
                assert Post.objects(id=post.id).get().content == form["content"]
                assert Post.objects(id=post.id).get().tag == form["tag"]
                assert Post.objects(id=post.id).get().notice == form["notice"]
                assert not Post.objects(id=post.id).get().is_deleted


    class Test_Like_Post:
        @pytest.fixture
        def trans_api(self, client, headers, board, post):
            return client.post(f'/boards/{str(board.id)}/posts/{str(post.id)}/like', headers=headers)

        class Context_정상_요청:
            def test_상태코드_201(self, trans_api):
                assert trans_api.status_code == 201

            def test_데이터_확인(self, trans_api, post, logged_in_user):
                assert logged_in_user in Post.objects(id=post.id).get().like

        class Context_이미_좋아요가_눌러져_있을_경우:
            @pytest.fixture
            def post(self, logged_in_user, board):
                return PostFactory.create(board=board, writer=logged_in_user.email, like=[logged_in_user])

            def test_상태코드_409(self, trans_api):
                assert trans_api.status_code == 409

            def test_데이터_확인(self, trans_api, post, logged_in_user):
                assert logged_in_user in Post.objects(id=post.id).get().like

    class Test_UnLike_Post:
        @pytest.fixture
        def trans_api(self, client, headers, board, post):
            return client.delete(f'/boards/{str(board.id)}/posts/{str(post.id)}/like', headers=headers)

        @pytest.fixture
        def post(self, logged_in_user, board):
            return PostFactory.create(board=board, writer=logged_in_user.email, like=[logged_in_user])
        class Context_정상_요청:
            def test_상태코드_204(self, trans_api):
                assert trans_api.status_code == 204

            def test_데이터_확인(self, trans_api, post, logged_in_user):
                assert logged_in_user not in Post.objects(id=post.id).get().like

        class Context_좋아요가_눌러져_있지_않은_경우:
            @pytest.fixture
            def post(self, logged_in_user, board):
                return PostFactory.create(board=board, writer=logged_in_user.email, like=[])

            def test_상태코드_412(self, trans_api):
                assert trans_api.status_code == 412

            def test_데이터_확인(self, trans_api, post, logged_in_user):
                assert logged_in_user not in Post.objects(id=post.id).get().like

    class Test_Search_Post:
        @pytest.fixture
        def form(self, post):
            return {
                "search_word": post.title
            }

        @pytest.fixture
        def trans_api(self, form, client, headers, board, post):
            return client.post(f'/boards/{str(board.id)}/posts/search', data=dumps(form), headers=headers)

        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post):
                assert len(trans_api.json) == 1
                assert trans_api.json[0]["title"] == post.title
                assert trans_api.json[0]["id"] == str(post.id)
                assert trans_api.json[0]["writer_email"] == post.writer.email
                assert trans_api.json[0]["date"] == post.date.isoformat(timespec='microseconds')
                assert trans_api.json[0]["content"] == post.content
                assert trans_api.json[0]["tag"] == post.tag
                assert trans_api.json[0]["notice"] == post.notice
                assert trans_api.json[0]["num_like"] == len(post.like)
                assert trans_api.json[0]["num_comment"] == post.num_comment
                assert not Post.objects(id=post.id).get().is_deleted

        class Context_제목에서_찾은_경우:
            @pytest.fixture
            def form(self):
                return {
                    "search_word": "title"
                }

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post, form):
                assert len(trans_api.json) == 1
                assert trans_api.json[0]["title"] == post.title
                assert form["search_word"] in trans_api.json[0]["title"]
                assert trans_api.json[0]["id"] == str(post.id)
                assert trans_api.json[0]["writer_email"] == post.writer.email
                assert trans_api.json[0]["date"] == post.date.isoformat(timespec='microseconds')
                assert trans_api.json[0]["content"] == post.content
                assert trans_api.json[0]["tag"] == post.tag
                assert trans_api.json[0]["notice"] == post.notice
                assert trans_api.json[0]["num_like"] == len(post.like)
                assert trans_api.json[0]["num_comment"] == post.num_comment
                assert not Post.objects(id=post.id).get().is_deleted

        class Context_내용에서_찾은_경우:
            @pytest.fixture
            def form(self):
                return {
                    "search_word": "content"
                }

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post, form):
                assert len(trans_api.json) == 1
                assert trans_api.json[0]["title"] == post.title
                assert form["search_word"] in trans_api.json[0]["content"]
                assert trans_api.json[0]["id"] == str(post.id)
                assert trans_api.json[0]["writer_email"] == post.writer.email
                assert trans_api.json[0]["date"] == post.date.isoformat(timespec='microseconds')
                assert trans_api.json[0]["content"] == post.content
                assert trans_api.json[0]["tag"] == post.tag
                assert trans_api.json[0]["notice"] == post.notice
                assert trans_api.json[0]["num_like"] == len(post.like)
                assert trans_api.json[0]["num_comment"] == post.num_comment
                assert not Post.objects(id=post.id).get().is_deleted

    class Test_Get_List:
        @pytest.fixture
        def post(self, logged_in_user, board):
            return [PostFactory.create(like=random.choice([[], [logged_in_user]]), notice=random.choice([True, False]),
                                       board=board) for _ in range(20)]

        @pytest.fixture
        def trans_api(self, client, board, headers, post):
            return client.get(f"/boards/{str(board.id)}/posts/?page=1&size=10", headers=headers)

        class Context_정상_요청:
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api):
                posts = trans_api.json
                for i in posts:
                    assert "id" in i
                    assert "writer_email" in i
                    assert "date" in i
                    assert "title" in i
                    assert "content" in i
                    assert "tag" in i
                    assert "notice" in i
                    assert "num_like" in i
                    assert "num_comment" in i
                    assert not Post.objects(id=i["id"]).get().is_deleted

            def test_공지사항_상단_노출_여부(self, trans_api):
                posts = trans_api.json
                for i in range(1, len(posts)):
                    assert (posts[i - 1]["notice"] == True and posts[i]["notice"] == True) or (
                            posts[i - 1]["notice"] == False and posts[i]["notice"] == False) \
                           or (posts[i - 1]["notice"] == True and posts[i]["notice"] == False)

            def test_존재_여부(self, trans_api, post):
                posts = trans_api.json
                for i in posts:
                    assert next((True for item in post if str(item.id) == i["id"]), False)

            def test_좋아요_누름_여부(self, trans_api, logged_in_user):
                posts = trans_api.json
                for i in posts:
                    assert (logged_in_user in Post.objects(id=i["id"]).get().like) == i["is_like"]

        class Context_페이지_인덱스가_음수일_경우:
            @pytest.fixture
            def trans_api(self, client, board, headers):
                return client.get(f"/boards/{str(board.id)}/posts/?page=-1&size=10", headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

        class Context_페이지_인덱스가_매우_클경우:
            @pytest.fixture
            def trans_api(self, client, board, headers):
                return client.get(f"/boards/{str(board.id)}/posts/?page=100&size=10", headers=headers)

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_빈리스트_반환(self, trans_api):
                assert trans_api.json == []
