import aimmoPost.aimmoPost as ai
import pytest
import json


@pytest.fixture
def api():
    test_api = ai.app
    api = test_api.test_client()
    return api


def test_get_post_detail_success(api):
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

    resp = api.get("/post/?id=" + data["_id"]["$oid"], content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]
    data = data["message"]
    assert isinstance(data["writer"], str) and len(data["writer"]) > 0
    assert isinstance(data["date"], str) and len(data["date"]) > 0
    assert isinstance(data["title"], str) and len(data["title"]) > 0
    assert isinstance(data["content"], str) and len(data["content"]) > 0
    assert isinstance(data["tag"], list)
    assert isinstance(data["notice"], bool)
    assert isinstance(data["comment"], list)
    assert isinstance(data["like"], list)


def test_get_post_detail_nosearch(api):
    resp = api.get("/post/?id=62bd246c90e2c3123635ed2d3", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not data["success"]
