import pytest
import jwt
import random
from app.models import Board, Post
from app.config import TestConfig
from tests.factory.user_factory import UserFactory
from tests.factory.board_factory import BoardFactory
from tests.factory.post_factory import PostFactory
from json import dumps


class Test_BoardView:
    @pytest.fixture
    def login_user(self):
        return UserFactory.create(is_master=True)

    @pytest.fixture
    def token(self, login_user):
        return jwt.encode({"user_id": login_user["user_id"], "is_master": login_user["is_master"]},
                          TestConfig.TOKEN_KEY, TestConfig.ALGORITHM)

    @pytest.fixture
    def board(self):
        return BoardFactory.create()

    class Test_Make_Board:
        @pytest.fixture
        def form(self):
            return {
                "board_name": "test_make_board_name"
            }

        @pytest.fixture
        def trans_api(self, form, client, token, headers):
            return client.post('/boards/', data=dumps(form), headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_데이터_삽입여부(self, trans_api, form):
            assert len(Board.objects(board_name=form["board_name"])) == 1

        class Test_이미_존재하는_게시판일_경우:
            @pytest.fixture
            def form(self, board):
                return {
                    "board_name": board.board_name
                }

            def test_상태코드_409(self, trans_api):
                assert trans_api.status_code == 409

    class Test_Get_Board_List:
        @pytest.fixture
        def trans_api(self, client, board):
            return client.get('/boards/', content_type="application/json")

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_게시판_리스트(self, trans_api, board):
            assert len(trans_api.json) == 1
            assert trans_api.json[0]["board_name"] == board.board_name

    class Test_Update_Board:
        @pytest.fixture
        def form(self):
            return {
                "board_name": "test_update_board_name"
            }

        @pytest.fixture
        def trans_api(self, client, board, headers, form):
            return client.put(f"/boards/{str(board.id)}", data=dumps(form), headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_업데이트_정보(self, board, trans_api, form):
            assert Board.objects(id=board.id).get().board_name == form["board_name"]

        class Test_마스터계정이_아닌_경우:
            @pytest.fixture
            def login_user(self):
                return UserFactory.create(is_master=False)

            @pytest.fixture
            def token(self, login_user):
                return jwt.encode(
                    {"user_id": login_user["user_id"], "is_master": login_user["is_master"]},
                    TestConfig.TOKEN_KEY, TestConfig.ALGORITHM)

            def test_상태코드_403(self, trans_api):
                assert trans_api.status_code == 403

            def test_massage_허가되지_않은_사용자입니다(self, trans_api):
                assert trans_api.json["message"] == '허가되지 않은 사용자입니다.'

        class Test_중복된_이름으로_수정하는_경우:
            @pytest.fixture
            def form(self, board):
                return {
                    "board_name": board.board_name
                }

            def test_상태코드_409(self, trans_api):
                assert trans_api.status_code == 409

            def test_message_이미_등록된_게시판입니다(self, trans_api):
                assert trans_api.json["message"] == "이미 등록된 게시판입니다."

    class Test_Delete_Board:
        @pytest.fixture
        def trans_api(self, client, board, headers):
            return client.delete(f"/boards/{str(board.id)}", headers=headers)

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_삭제_여부(self, board, trans_api):
            assert len(Board.objects(id=board.id)) == 0
