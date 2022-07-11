import pytest
import jwt
import uuid
from bson import ObjectId
from json import dumps
from app.models import Post
from app.config import TestConfig
from tests.factory.user_factory import UserFactory
from tests.factory.board_factory import BoardFactory
from tests.factory.post_factory import PostFactory


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

        def test_데이터_확인(self,trans_api, form):
            assert Post.objects()[0].title == form["title"]
            assert Post.objects()[0].content == form["content"]
            assert Post.objects()[0].tag == form["tag"]
            assert Post.objects()[0].notice == form["notice"]

        class Test_로그인이_되어있지_않은_경우:
            @pytest.fixture
            def headers(self):
                return {
                    'Content-Type': 'application/json'
                }

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_로그인하지_않은_사용자입니다(self, trans_api):
                assert trans_api.json["message"] == "로그인하지 않은 사용자입니다."

        class Test_유효하지_않은_토큰일_경우:
            @pytest.fixture
            def token(self):
                return uuid.uuid4()

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_유효하지_않은_토큰입니다(self, trans_api):
                assert trans_api.json["message"] == '유효하지 않은 토큰입니다.'

        class Test_게시판이_없을_경우:
            @pytest.fixture
            def trans_api(self, form, client, headers, board):
                return client.post(f'/boards/{ObjectId()}/posts/', data=dumps(form), headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

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

        class Test_로그인이_되어있지_않은_경우:
            @pytest.fixture
            def headers(self):
                return {
                    'Content-Type': 'application/json'
                }

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_로그인하지_않은_사용자입니다(self, trans_api):
                assert trans_api.json["message"] == "로그인하지 않은 사용자입니다."

        class Test_유효하지_않은_토큰일_경우:
            @pytest.fixture
            def token(self):
                return uuid.uuid4()

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_유효하지_않은_토큰입니다(self, trans_api):
                assert trans_api.json["message"] == '유효하지 않은 토큰입니다.'

        class Test_게시판이_없을_경우:
            @pytest.fixture
            def trans_api(self, client, headers, board, post):
                return client.get(f'/boards/{ObjectId()}/posts/{post.id}', headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

        class Test_게시물이_없을_경우:
            @pytest.fixture
            def trans_api(self, client, headers, board, post):
                return client.get(f'/boards/{board.id}/posts/{ObjectId()}', headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

    class Test_Delete_Post:
        @pytest.fixture
        def trans_api(self, client, board, headers, post):
            return client.delete(f"/boards/{str(board.id)}/posts/{str(post.id)}", headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_삭제_여부(self, post, trans_api):
            assert len(Post.objects(id=post.id)) == 0

        class Test_로그인이_되어_있지_않은_경우:
            @pytest.fixture
            def headers(self):
                return {
                    'Content-Type': 'application/json'
                }

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_로그인하지_않은_사용자입니다(self, trans_api):
                assert trans_api.json["message"] == "로그인하지 않은 사용자입니다."

        class Test_유효하지_않은_토큰일_경우:
            @pytest.fixture
            def token(self):
                return uuid.uuid4()

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_유효하지_않은_토큰입니다(self, trans_api):
                assert trans_api.json["message"] == '유효하지 않은 토큰입니다.'

        class Test_없는_게시판일_경우:

            @pytest.fixture
            def trans_api(self, client, board, headers, post):
                return client.delete(f"/boards/{ObjectId()}/posts/{str(post.id)}", headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

            def test_message_없는_게시판입니다(self, trans_api):
                assert trans_api.json["message"] == "없는 게시판입니다"

        class Test_없는_게시물일_경우:

            @pytest.fixture
            def trans_api(self, client, board, headers, post):
                return client.delete(f"/boards/{board.id}/posts/{ObjectId()}", headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

            def test_message_없는_게시물입니다(self, trans_api):
                assert trans_api.json["message"] == "없는 게시물입니다"

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

        def test_데이터_확인(self,trans_api, form, post):
            assert Post.objects(id=post.id).get().title == form["title"]
            assert Post.objects(id=post.id).get().content == form["content"]
            assert Post.objects(id=post.id).get().tag == form["tag"]
            assert Post.objects(id=post.id).get().notice == form["notice"]

        class Test_로그인이_되어있지_않은_경우:
            @pytest.fixture
            def headers(self):
                return {
                    'Content-Type': 'application/json'
                }

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_로그인하지_않은_사용자입니다(self, trans_api):
                assert trans_api.json["message"] == "로그인하지 않은 사용자입니다."

        class Test_유효하지_않은_토큰일_경우:
            @pytest.fixture
            def token(self):
                return uuid.uuid4()

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_유효하지_않은_토큰입니다(self, trans_api):
                assert trans_api.json["message"] == '유효하지 않은 토큰입니다.'

        class Test_작성_계정이_아닐_경우:
            @pytest.fixture
            def login_wrong_user(self):
                return UserFactory.create(user_id="wrong_test_id")

            @pytest.fixture
            def token(self, login_wrong_user):
                return jwt.encode({"user_id": login_wrong_user["user_id"], "is_master": login_wrong_user["is_master"]},
                                  TestConfig.TOKEN_KEY, TestConfig.ALGORITHM)

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_유효하지_않은_토큰입니다(self, trans_api):
                assert trans_api.json["message"] == '작성자 아이디가 아닙니다.'

        class Test_게시판이_없을_경우:
            @pytest.fixture
            def trans_api(self, form, client, headers, board, post):
                return client.put(f'/boards/{ObjectId()}/posts/{str(post.id)}', data=dumps(form), headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

            def test_message_없는_게시판입니다(self, trans_api):
                assert trans_api.json["message"] == "없는 게시판입니다"

        class Test_게시물이_없을_경우:
            @pytest.fixture
            def trans_api(self, form, client, headers, board, post):
                return client.put(f'/boards/{str(board.id)}/posts/{ObjectId()}', data=dumps(form), headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

            def test_message_없는_게시물입니다(self, trans_api):
                assert trans_api.json["message"] == "없는 게시물입니다"

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

        def test_데이터_확인(self,trans_api, post, login_user):
            assert login_user in Post.objects(id=post.id).get().like

        class Test_이미_좋아요가_눌러져_있을_경우:
            @pytest.fixture
            def post(self, login_user, board):
                return PostFactory.create(board=board, writer=login_user.user_id, like=[login_user])

            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post, login_user):
                assert login_user not in Post.objects(id=post.id).get().like

        class Test_로그인이_되어있지_않은_경우:
            @pytest.fixture
            def headers(self):
                return {
                    'Content-Type': 'application/json'
                }

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_로그인하지_않은_사용자입니다(self, trans_api):
                assert trans_api.json["message"] == "로그인하지 않은 사용자입니다."

        class Test_유효하지_않은_토큰일_경우:
            @pytest.fixture
            def token(self):
                return uuid.uuid4()

            def test_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

            def test_massage_유효하지_않은_토큰입니다(self, trans_api):
                assert trans_api.json["message"] == '유효하지 않은 토큰입니다.'

        class Test_게시판이_없을_경우:
            @pytest.fixture
            def trans_api(self, client, headers, board, post):
                return client.post(f'/boards/{ObjectId()}/posts/{str(post.id)}/like', headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

            def test_message_없는_게시판입니다(self, trans_api):
                assert trans_api.json["message"] == "없는 게시판입니다"

        class Test_게시물이_없을_경우:
            @pytest.fixture
            def trans_api(self, client, headers, board, post):
                return client.post(f'/boards/{str(board.id)}/posts/{ObjectId()}/like', headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

            def test_message_없는_게시물입니다(self, trans_api):
                assert trans_api.json["message"] == "없는 게시물입니다"

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
            assert len(trans_api.json["post_list"]) == 1
            assert trans_api.json["post_list"][0]["title"] == post.title
            assert trans_api.json["post_list"][0]["id"] == str(post.id)
            assert trans_api.json["post_list"][0]["writer"] == post.writer
            assert trans_api.json["post_list"][0]["date"] == post.date.isoformat(timespec='microseconds')
            assert trans_api.json["post_list"][0]["content"] == post.content
            assert trans_api.json["post_list"][0]["tag"] == post.tag
            assert trans_api.json["post_list"][0]["notice"] == post.notice
            assert trans_api.json["post_list"][0]["num_like"] == len(post.like)
            assert trans_api.json["post_list"][0]["num_comment"] == post.num_comment

        class Test_제목에서_찾은_경우:
            @pytest.fixture
            def form(self):
                return {
                    "search_word": "title"
                }
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post, form):
                assert len(trans_api.json["post_list"]) == 1
                assert trans_api.json["post_list"][0]["title"] == post.title
                assert form["search_word"] in trans_api.json["post_list"][0]["title"]
                assert trans_api.json["post_list"][0]["id"] == str(post.id)
                assert trans_api.json["post_list"][0]["writer"] == post.writer
                assert trans_api.json["post_list"][0]["date"] == post.date.isoformat(timespec='microseconds')
                assert trans_api.json["post_list"][0]["content"] == post.content
                assert trans_api.json["post_list"][0]["tag"] == post.tag
                assert trans_api.json["post_list"][0]["notice"] == post.notice
                assert trans_api.json["post_list"][0]["num_like"] == len(post.like)
                assert trans_api.json["post_list"][0]["num_comment"] == post.num_comment

        class Test_내용에서_찾은_경우:
            @pytest.fixture
            def form(self):
                return {
                    "search_word": "content"
                }
            def test_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_데이터_확인(self, trans_api, post, form):
                assert len(trans_api.json["post_list"]) == 1
                assert trans_api.json["post_list"][0]["title"] == post.title
                assert form["search_word"] in trans_api.json["post_list"][0]["content"]
                assert trans_api.json["post_list"][0]["id"] == str(post.id)
                assert trans_api.json["post_list"][0]["writer"] == post.writer
                assert trans_api.json["post_list"][0]["date"] == post.date.isoformat(timespec='microseconds')
                assert trans_api.json["post_list"][0]["content"] == post.content
                assert trans_api.json["post_list"][0]["tag"] == post.tag
                assert trans_api.json["post_list"][0]["notice"] == post.notice
                assert trans_api.json["post_list"][0]["num_like"] == len(post.like)
                assert trans_api.json["post_list"][0]["num_comment"] == post.num_comment

        class Test_게시판이_없을_경우:
            @pytest.fixture
            def trans_api(self, client, headers, board, post):
                return client.post(f'/boards/{ObjectId()}/posts/search', headers=headers)

            def test_상태코드_404(self, trans_api):
                assert trans_api.status_code == 404

            def test_message_없는_게시물입니다(self, trans_api):
                assert trans_api.json["message"] == "없는 게시판입니다"
