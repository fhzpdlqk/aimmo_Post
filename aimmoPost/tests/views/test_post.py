import pytest
import jwt
import uuid
import random
from bson import ObjectId
from json import dumps
from app.models import Post
from app.config import TestConfig
from tests.factory.user_factory import UserFactory
from tests.factory.board_factory import BoardFactory
from tests.factory.post_factory import PostFactory
from tests.factory.comment_factory import CommentFactory


class Test_PostView:
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
        return PostFactory.create(board=board, writer=login_user.user_id)

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

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_삽입여부(self, trans_api, form):
            assert len(Post.objects()) == 1

        def test_데이터_확인(self, trans_api, form):
            assert Post.objects()[0].title == form["title"]
            assert Post.objects()[0].content == form["content"]
            assert Post.objects()[0].tag == form["tag"]
            assert Post.objects()[0].notice == form["notice"]

        class Test_제목이_누락되었을_경우:
            @pytest.fixture
            def form(self):
                return {
                    "content": "make_post_content",
                    "tag": ["make_tag_1", "make_tag_2"],
                    "notice": True
                }

            def test_상태코드_422(self, trans_api):
                assert trans_api.status_code == 422

        class Test_내용이_누락되었을_경우:
            @pytest.fixture
            def form(self):
                return {
                    "title": "make_post_title",
                    "tag": ["make_tag_1", "make_tag_2"],
                    "notice": True
                }

            def test_상태코드_422(self, trans_api):
                assert trans_api.status_code == 422

        class Test_태그가_누락되었을_경우:
            @pytest.fixture
            def form(self):
                return {
                    "title": "make_post_title",
                    "content": "make_post_content",
                    "notice": True
                }

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_삽입여부(self, trans_api, form):
                assert len(Post.objects()) == 1

            def test_데이터_확인(self, trans_api, form):
                assert Post.objects()[0].title == form["title"]
                assert Post.objects()[0].content == form["content"]
                assert Post.objects()[0].tag == []
                assert Post.objects()[0].notice == form["notice"]

        class Test_공지여부가_누락되었을_경우:
            @pytest.fixture
            def form(self):
                return {
                    "title": "make_post_title",
                    "content": "make_post_content",
                    "tag": ["make_tag_1", "make_tag_2"]
                }

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_삽입여부(self, trans_api, form):
                assert len(Post.objects()) == 1

            def test_데이터_확인(self, trans_api, form):
                assert Post.objects()[0].title == form["title"]
                assert Post.objects()[0].content == form["content"]
                assert Post.objects()[0].tag == form["tag"]
                assert Post.objects()[0].notice == False

    class Test_Get_Post:
        @pytest.fixture
        def trans_api(self, client, headers, board, post):
            return client.get(f'/boards/{str(board.id)}/posts/{str(post.id)}', headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api, post):
            assert str(post.id) == trans_api.json["id"]
            assert post.title == trans_api.json["title"]
            assert post.content == trans_api.json["content"]
            assert post.writer == trans_api.json["writer"]
            assert post.notice == trans_api.json["notice"]
            assert len(post.like) == trans_api.json["num_like"]
            assert post.tag == trans_api.json["tag"]
            assert post.date.isoformat(timespec='microseconds') == trans_api.json["date"]
            assert post.num_comment == trans_api.json["num_comment"]
            assert trans_api.json["comment"] == []

    class Test_Delete_Post:
        @pytest.fixture
        def trans_api(self, client, board, headers, post):
            return client.delete(f"/boards/{str(board.id)}/posts/{str(post.id)}", headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_삭제_여부(self, post, trans_api):
            assert len(Post.objects(id=post.id)) == 0

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

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api, form, post):
            assert Post.objects(id=post.id).get().title == form["title"]
            assert Post.objects(id=post.id).get().content == form["content"]
            assert Post.objects(id=post.id).get().tag == form["tag"]
            assert Post.objects(id=post.id).get().notice == form["notice"]

        class Test_제목이_누락되었을_경우:
            @pytest.fixture
            def form(self):
                return {
                    "content": "make_post_content",
                    "tag": ["make_tag_1", "make_tag_2"],
                    "notice": True
                }

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, form, post):
                assert Post.objects(id=post.id).get().title == post.title
                assert Post.objects(id=post.id).get().content == form["content"]
                assert Post.objects(id=post.id).get().tag == form["tag"]
                assert Post.objects(id=post.id).get().notice == form["notice"]

        class Test_내용이_누락되었을_경우:
            @pytest.fixture
            def form(self):
                return {
                    "title": "make_post_title",
                    "tag": ["make_tag_1", "make_tag_2"],
                    "notice": True
                }

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, form, post):
                assert Post.objects(id=post.id).get().title == form["title"]
                assert Post.objects(id=post.id).get().content == post.content
                assert Post.objects(id=post.id).get().tag == form["tag"]
                assert Post.objects(id=post.id).get().notice == form["notice"]

        class Test_태그가_누락되었을_경우:
            @pytest.fixture
            def form(self):
                return {
                    "title": "make_post_title",
                    "content": "make_post_content",
                    "notice": True
                }

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, form, post):
                assert Post.objects(id=post.id).get().title == form["title"]
                assert Post.objects(id=post.id).get().content == form["content"]
                assert Post.objects(id=post.id).get().tag == post.tag
                assert Post.objects(id=post.id).get().notice == form["notice"]

        class Test_공지여부가_누락되었을_경우:
            @pytest.fixture
            def form(self):
                return {
                    "title": "make_post_title",
                    "content": "make_post_content",
                    "tag": ["make_tag_1", "make_tag_2"]
                }

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, form, post):
                assert Post.objects(id=post.id).get().title == form["title"]
                assert Post.objects(id=post.id).get().content == form["content"]
                assert Post.objects(id=post.id).get().tag == form["tag"]
                assert Post.objects(id=post.id).get().notice == post.notice

    class Test_Like_Post:
        @pytest.fixture
        def trans_api(self, client, headers, board, post):
            return client.post(f'/boards/{str(board.id)}/posts/{str(post.id)}/like', headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api, post, login_user):
            assert login_user in Post.objects(id=post.id).get().like

        class Test_이미_좋아요가_눌러져_있을_경우:
            @pytest.fixture
            def post(self, login_user, board):
                return PostFactory.create(board=board, writer=login_user.user_id, like=[login_user])

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post, login_user):
                assert login_user not in Post.objects(id=post.id).get().like

    class Test_Search_Post:
        @pytest.fixture
        def form(self):
            return {
                "search_word": "sample"
            }

        @pytest.fixture
        def trans_api(self, form, client, headers, board, post):
            return client.post(f'/boards/{str(board.id)}/posts/search', data=dumps(form), headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api, post):
            assert len(trans_api.json) == 1
            assert trans_api.json[0]["title"] == post.title
            assert trans_api.json[0]["id"] == str(post.id)
            assert trans_api.json[0]["writer"] == post.writer
            assert trans_api.json[0]["date"] == post.date.isoformat(timespec='microseconds')
            assert trans_api.json[0]["content"] == post.content
            assert trans_api.json[0]["tag"] == post.tag
            assert trans_api.json[0]["notice"] == post.notice
            assert trans_api.json[0]["num_like"] == len(post.like)
            assert trans_api.json[0]["num_comment"] == post.num_comment

        class Test_제목에서_찾은_경우:
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
                assert trans_api.json[0]["writer"] == post.writer
                assert trans_api.json[0]["date"] == post.date.isoformat(timespec='microseconds')
                assert trans_api.json[0]["content"] == post.content
                assert trans_api.json[0]["tag"] == post.tag
                assert trans_api.json[0]["notice"] == post.notice
                assert trans_api.json[0]["num_like"] == len(post.like)
                assert trans_api.json[0]["num_comment"] == post.num_comment

        class Test_내용에서_찾은_경우:
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
                assert trans_api.json[0]["writer"] == post.writer
                assert trans_api.json[0]["date"] == post.date.isoformat(timespec='microseconds')
                assert trans_api.json[0]["content"] == post.content
                assert trans_api.json[0]["tag"] == post.tag
                assert trans_api.json[0]["notice"] == post.notice
                assert trans_api.json[0]["num_like"] == len(post.like)
                assert trans_api.json[0]["num_comment"] == post.num_comment

    class Test_Get_List:
        @pytest.fixture
        def post(self, login_user, board):
            return [PostFactory.create(like=random.choice([[], [login_user]]), notice=random.choice([True, False]),
                                       board=board) for _ in range(20)]

        @pytest.fixture
        def trans_api(self, client, board, headers, post):
            return client.get(f"/boards/{str(board.id)}/posts/?page=1&size=10", headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_확인(self, trans_api):
            posts = trans_api.json
            for i in posts:
                assert "id" in i
                assert "writer" in i
                assert "date" in i
                assert "title" in i
                assert "content" in i
                assert "tag" in i
                assert "notice" in i
                assert "num_like" in i
                assert "num_comment" in i

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

        def test_좋아요_누름_여부(self, trans_api, login_user):
            posts = trans_api.json
            for i in posts:
                assert (login_user in Post.objects(id=i["id"]).get().like) == i["is_like"]

        class Test_페이지_인덱스가_음수일_경우:
            @pytest.fixture
            def trans_api(self, client, board, headers):
                return client.get(f"/boards/{str(board.id)}/posts/?page=-1&size=10", headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

        class Test_페이지_인덱스가_매우_클경우:
            @pytest.fixture
            def trans_api(self, client, board, headers):
                return client.get(f"/boards/{str(board.id)}/posts/?page=100&size=10", headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 200

            def test_빈리스트_반환(self, trans_api):
                assert trans_api.json == []
