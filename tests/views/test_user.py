import pytest
import factory
import bcrypt
import jwt
from app.models import User
from app.config import TestConfig
from tests.factory.user_factory import UserFactory
from json import dumps
from faker import Faker


class Describe_UserView:

    class Describe_Signup:
        @pytest.fixture
        def form(self):
            return {
                "email": Faker().email(),
                "password": factory.Faker("password").provider
            }

        @pytest.fixture
        def trans_api(self, form, client):
            return client.post('/users/', data=dumps(form), content_type="application/json")

        class Context_정상_요청:
            def test_상태코드_201(self, trans_api):
                assert trans_api.status_code == 201

            def test_user_수가_증가(self, trans_api):
                assert User.objects().count() == 1

            def test_데이터베이스에_존재(self, trans_api, form):
                assert len(User.objects(email=form["email"])) == 1

        class Context_중복된_id로_회원가입할_경우:
            @pytest.fixture
            def form(self, logged_in_user):
                return {
                    "email": logged_in_user.email,
                    "password": factory.Faker("password").provider
                }

            def test_상태코드_409(self, trans_api):
                assert trans_api.status_code == 409


    class Describe_Login:
        @pytest.fixture
        def created_user(self):
            return UserFactory(email="test@naver.com",
                               password=bcrypt.hashpw("test_signup_user_pw".encode("utf-8"), bcrypt.gensalt()))

        @pytest.fixture
        def form(self, logged_in_user):
            return {
                "email": logged_in_user.email,
                "password": "test_user_pw"
            }

        @pytest.fixture
        def trans_api(self, form, client, logged_in_user):
            return client.post('/users/login', data=dumps(form), content_type="application/json")

        class Context_정상_요청:
            def test_login_상태코드_200(self, trans_api):
                assert trans_api.status_code == 200

            def test_login_토큰일치(self, trans_api, form, created_user):
                token = jwt.encode({"email": form["email"], "is_master": created_user.is_master}, TestConfig.TOKEN_KEY,
                                   TestConfig.ALGORITHM)
                assert token == trans_api.json["token"]

        class Context_아이디가_없을경우:
            @pytest.fixture
            def form(self):
                return {
                    "email": "test@naver.com",
                    "password": "test_user_pw"
                }

            def test_login_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

        class Context_비밀번호가_틀렸을경우:
            @pytest.fixture
            def form(self, logged_in_user):
                return {
                    "email": logged_in_user.email,
                    "password": "test_user_wrong_pw"
                }

            def test_login_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401

    class Describe_Put:

        @pytest.fixture
        def form(self):
            return {
                "origin_password": "test_user_pw",
                "password": "test_update_user_pw"
            }

        @pytest.fixture
        def trans_api(self, form, headers, client, logged_in_user):
            return client.put('/users/', data=dumps(form), headers=headers)

        class Context_정상_요청:

            def test_상태코드_201(self, trans_api):
                assert trans_api.status_code == 201

            def test_변경_확인(self, trans_api, logged_in_user, form):
                assert bcrypt.checkpw(form["password"].encode("utf-8"), User.objects(email=logged_in_user.email).get().password.encode("utf-8"))

        class Context_동일한_비밀번호로_요청할_경우:

            @pytest.fixture
            def form(self, logged_in_user):
                return {
                    "origin_password": "test_user_pw",
                    "password": "test_user_pw"
                }
            def test_상태코드_200(self, trans_api, logged_in_user):
                assert trans_api.status_code == 409

