import aimmoPost.aimmoPost as ai
import pytest
import json


@pytest.fixture
def api():
    test_api = ai.app
    api = test_api.test_client()
    return api


def test_comment_update_success(api):
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

    new_data = {"content": "samplecontent333"}
    resp = api.post(f"/comment/regist?id={data['id']}", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]

    resp = api.get("/post/?id=" + data["id"], content_type="application/json")
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

    comment_id = data["comment"][0]["id"]
    new_data = {"content": "samplecontent4444"}
    resp = api.put(f"/comment/?comment_id={comment_id}", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    print(resp.status_code)
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]


def test_comment_update_nocomment(api):
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

    new_data = {"content": "samplecontent333"}
    resp = api.post(f"/comment/regist?id={data['id']}", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]

    resp = api.get("/post/?id=" + data["id"], content_type="application/json")
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

    comment_id = data["comment"][0]["id"]
    new_data = {}
    resp = api.put(f"/comment/?comment_id={comment_id}", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    print(resp.status_code)
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not datas["success"]


def test_comment_update_difparams(api):
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

    new_data = {"content": "samplecontent333"}
    resp = api.post(f"/comment/regist?id={data['id']}", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]

    resp = api.get("/post/?id=" + data["id"], content_type="application/json")
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

    comment_id = data["comment"][0]["id"]
    new_data = {"content": "samplecontent4444"}
    resp = api.put(f"/comment/?id={comment_id}", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    print(resp.status_code)
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not datas["success"]
