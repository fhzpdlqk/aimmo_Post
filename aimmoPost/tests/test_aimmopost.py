import aimmoPost.aimmoPost as ai
import pytest
import json


def test_version():
    assert ai.__version__ == "0.1.0"


@pytest.fixture
def api():
    test_api = ai.app
    api = test_api.test_client()
    return api


def test_signup_duplicate(api):
    new_user = {"user_id": "testid", "user_pw": "testpw"}
    resp = api.post("/user/", data=json.dumps(new_user), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"message": "id가 중복되었습니다.", "success": False}


def test_signup_nopw(api):
    new_user = {"user_id": "testid"}
    resp = api.post("/user/", data=json.dumps(new_user), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"message": "<class 'KeyError'>", "success": False}


def test_signup_noid(api):
    new_user = {"user_pw": "testpw"}
    resp = api.post("/user/", data=json.dumps(new_user), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"message": "<class 'KeyError'>", "success": False}
