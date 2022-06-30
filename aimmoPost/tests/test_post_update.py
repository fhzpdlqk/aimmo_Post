import aimmoPost.aimmoPost as ai
import pytest
import json


@pytest.fixture
def api():
    test_api = ai.app
    api = test_api.test_client()
    return api


def test_post_update_success(api):
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

    new_data = {"title": "sampletitle222", "content": "samplecontent222", "tag": ["st_1", "st_2"], "notice": True}
    resp = api.put("/post/?id=" + data["_id"]["$oid"], data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]


def test_post_update_wronguser(api):
    login_data = {"user_id": "admin2", "user_pw": "admin"}
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

    new_data = {"title": "sampletitle222", "content": "samplecontent222", "tag": ["st_1", "st_2"], "notice": True}
    resp = api.put("/post/?id=" + data["_id"]["$oid"], data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not datas["success"]


def test_post_update_notitle(api):
    login_data = {"user_id": "admin2", "user_pw": "admin"}
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

    new_data = {"content": "samplecontent222", "tag": ["st_1", "st_2"], "notice": True}
    resp = api.put("/post/?id=" + data["_id"]["$oid"], data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not datas["success"]


def test_post_update_nocontent(api):
    login_data = {"user_id": "admin2", "user_pw": "admin"}
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

    new_data = {"title": "sampletitle222", "tag": ["st_1", "st_2"], "notice": True}
    resp = api.put("/post/?id=" + data["_id"]["$oid"], data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not datas["success"]


def test_post_update_notag(api):
    login_data = {"user_id": "admin2", "user_pw": "admin"}
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

    new_data = {"title": "sampletitle222", "content": "samplecontent222", "notice": True}
    resp = api.put("/post/?id=" + data["_id"]["$oid"], data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not datas["success"]


def test_post_update_nonotice(api):
    login_data = {"user_id": "admin2", "user_pw": "admin"}
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

    new_data = {"title": "sampletitle222", "content": "samplecontent222", "tag": ["st_1", "st_2"]}
    resp = api.put("/post/?id=" + data["_id"]["$oid"], data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not datas["success"]
