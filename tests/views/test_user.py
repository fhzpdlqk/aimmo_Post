import pytest
import factory
import bcrypt
import jwt
from flask import url_for
from app.models import User
from app.config import TestConfig
from tests.factory.user_factory import UserFactory
from json import dumps


class Describe_UserView:
    @pytest.fixture
    def created_user(self):
        return UserFactory.create()

    class Describe_Post:
        @pytest.fixture
        def form(self):
            return {
                "user_id": factory.Faker("user_id").provider,
                "user_pw": factory.Faker("user_pw").provider
            }

        @pytest.fixture
        def trans_api(self, form, client):
            return client.post('/users/', data=dumps(form), content_type="application/json")

        def test_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_user_수가_증가(self, trans_api):
            assert User.objects().count() == 1

        def test_데이터베이스에_존재(self, trans_api, form):
            assert len(User.objects(user_id=form["user_id"])) == 1

        class Context_중복된_id로_회원가입할_경우:
            @pytest.fixture
            def form(self, created_user):
                return {
                    "user_id": created_user.user_id,
                    "user_pw": factory.Faker("user_pw").provider
                }

            def test_상태코드_409(self, trans_api):
                assert trans_api.status_code == 409

    class Describe_Login:
        @pytest.fixture
        def created_user(self):
            return UserFactory(user_id="test_signup_user_id",
                               user_pw=bcrypt.hashpw("test_signup_user_pw".encode("utf-8"), bcrypt.gensalt()))

        @pytest.fixture
        def form(self):
            return {
                "user_id": "test_signup_user_id",
                "user_pw": "test_signup_user_pw"
            }

        @pytest.fixture
        def trans_api(self, form, client, created_user):
            return client.post('/users/login', data=dumps(form), content_type="application/json")

        def test_login_상태코드_200(self, trans_api):
            assert trans_api.status_code == 200

        def test_login_토큰일치(self, trans_api, form, created_user):
            token = jwt.encode({"user_id": form["user_id"], "is_master": created_user.is_master}, TestConfig.TOKEN_KEY,
                               TestConfig.ALGORITHM)
            assert token == trans_api.json["token"]

        class Context_아이디가_없을경우:
            @pytest.fixture
            def form(self):
                return {
                    "user_id": "test_signup_user_no_id",
                    "user_pw": "test_signup_user_pw"
                }

            def test_login_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

        class Context_비밀번호가_틀렸을경우:
            @pytest.fixture
            def form(self):
                return {
                    "user_id": "test_signup_user_id",
                    "user_pw": "test_signup_user_wrong_pw"
                }

            def test_login_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

    class Describe_Put:
        @pytest.fixture
        def created_user(self):
            return UserFactory(user_id="test_signup_user_id",
                               user_pw=bcrypt.hashpw("test_signup_user_pw".encode("utf-8"), bcrypt.gensalt()))
        @pytest.fixture
        def token(self, created_user):
            return jwt.encode({"user_id": created_user["user_id"], "is_master": created_user["is_master"]},
                              TestConfig.TOKEN_KEY, TestConfig.ALGORITHM)
        @pytest.fixture
        def form(self):
            return {
                "user_origin_pw": "test_signup_user_pw",
                "user_pw": "test_update_user_pw"
            }

        @pytest.fixture
        def trans_api(self, form, headers, client, created_user):
            return client.put('/users/', data=dumps(form), headers=headers)

        def test_상태코드_200(self, trans_api, created_user):
            assert trans_api.status_code == 200

        def test_변경_확인(self, trans_api, created_user, form):
            assert bcrypt.checkpw(form["user_pw"].encode("utf-8"), User.objects(user_id=created_user.user_id).get().user_pw.encode("utf-8"))
