from aimmoPost import __version__, app
import pytest
import json

from ..models import User


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def api():
    test_api = app.app
    api = test_api.test_client()
    return api


async def test_signup(api):
    new_user = {"user_id": "testid", "user_pw": "testpw"}
    resp = await api.post("/user/", data=json.dumps(new_user), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"message": "id가 중복되었습니다.", "success": False}

    new_user = {"user_id": "testid"}
    resp = await api.post("/user/", data=json.dumps(new_user), content_type="application/json")
    assert resp.status_code == 200
    assert data == {"message": "<class 'KeyError'>", "success": False}

    new_user = {"user_pw": "testpw"}
    resp = await api.post("/user/", data=json.dumps(new_user), content_type="application/json")
    assert resp.status_code == 200
    assert data == {"message": "<class 'KeyError'>", "success": False}
