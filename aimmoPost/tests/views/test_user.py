import pytest
import factory
import bcrypt
import jwt
from app.models import User
from app.config import TestConfig
from tests.factory.user_factory import UserFactory
from json import dumps

class Test_UserView:
    @pytest.fixture
    def logged_in_user(self):
        return UserFactory.create()

    class Test_Signup_User:
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

        class Test_중복된_id로_회원가입:
            @pytest.fixture
            def form(self, logged_in_user):
                return {
                    "user_id": logged_in_user.user_id,
                    "user_pw": factory.Faker("user_pw").provider
                }

            def test_상태코드_409(self,trans_api):
                assert trans_api.status_code == 409

    class Test_Login_User:
        @pytest.fixture
        def signup_user(self):
            return UserFactory(user_id="test_signup_user_id", user_pw=bcrypt.hashpw("test_signup_user_pw".encode("utf-8"), bcrypt.gensalt()))
        @pytest.fixture
        def form(self):
            return {
                "user_id": "test_signup_user_id",
                "user_pw": "test_signup_user_pw",
                "is_master": False
            }

        @pytest.fixture
        def trans_api(self, form, client, signup_user):
            return client.post('/users/login', data=dumps(form), content_type="application/json")

        def test_login_상태코드_200(self, trans_api):
            assert trans_api.status_code==200

        def test_login_토큰일치(self, trans_api, form):
            token = jwt.encode({"user_id": form["user_id"], "is_master": form["is_master"]}, TestConfig.TOKEN_KEY, TestConfig.ALGORITHM)
            assert token == trans_api.json["token"]

        class Test_아이디가_없을경우:
            @pytest.fixture
            def form(self):
                return {
                    "user_id": "test_signup_user_no_id",
                    "user_pw": "test_signup_user_pw",
                    "is_master": False
                }
            def test_login_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401
        class Test_비밀번호가_틀렸을경우:
            @pytest.fixture
            def form(self):
                return {
                    "user_id": "test_signup_user_id",
                    "user_pw": "test_signup_user_wrong_pw",
                    "is_master": False
                }
            def test_login_상태코드_401(self, trans_api):
                assert trans_api.status_code == 401
