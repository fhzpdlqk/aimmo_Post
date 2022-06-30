import aimmoPost.aimmoPost as ai
import pytest
import json


@pytest.fixture
def api():
    test_api = ai.app
    api = test_api.test_client()
    return api


def test_comment_add_success(api):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = api.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True
    assert isinstance(data["token"], str)
    token = data["token"]

    resp = api.get("/post/list/?page=1", content_type="application/json")
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]
    data = datas["message"][0]

    new_data = {"content": "samplecontent222"}
    resp = api.post("/comment/regist?id=" + data["_id"]["$oid"], data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]


def test_comment_add_no_comment(api):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = api.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True
    assert isinstance(data["token"], str)
    token = data["token"]

    resp = api.get("/post/list/?page=1", content_type="application/json")
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]
    data = datas["message"][0]

    new_data = {}
    resp = api.post("/comment/regist?id=" + data["_id"]["$oid"], data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not datas["success"]
