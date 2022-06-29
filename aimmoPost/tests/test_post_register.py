import aimmoPost.aimmoPost as ai
import pytest
import json


@pytest.fixture
def api():
    test_api = ai.app
    api = test_api.test_client()
    return api


def test_regist_post_success(api):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = api.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True
    assert isinstance(data["token"], str)

    token = data["token"]
    new_data = {"title": "sampletitle", "content": "samplecontent", "tag": ["st_1", "st_2"], "notice": True}
    resp = api.post("/post/regist", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"success": True}


def test_regist_post_wrong_token(api):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = api.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True
    assert isinstance(data["token"], str)

    token = data["token"] + "a"
    new_data = {"title": "sampletitle", "content": "samplecontent", "tag": ["st_1", "st_2"], "notice": True}
    resp = api.post("/post/regist", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == False


def test_regist_post_no_title(api):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = api.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True
    assert isinstance(data["token"], str)

    token = data["token"]
    new_data = {"content": "samplecontent", "tag": ["st_1", "st_2"], "notice": True}
    resp = api.post("/post/regist", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == False


def test_regist_post_no_content(api):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = api.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True
    assert isinstance(data["token"], str)

    token = data["token"]
    new_data = {"title": "sampletitle", "tag": ["st_1", "st_2"], "notice": True}
    resp = api.post("/post/regist", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == False


def test_regist_post_no_tag(api):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = api.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True
    assert isinstance(data["token"], str)

    token = data["token"]
    new_data = {"title": "sampletitle", "content": "samplecontent", "notice": True}
    resp = api.post("/post/regist", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True


def test_regist_post_no_notice(api):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = api.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True
    assert isinstance(data["token"], str)

    token = data["token"]
    new_data = {"title": "sampletitle", "content": "samplecontent", "tag": ["st_1", "st_2"]}
    resp = api.post("/post/regist", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == False
