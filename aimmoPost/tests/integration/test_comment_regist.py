import pytest
import json
import uuid


@pytest.fixture
def new_data():
    return {"content": "samplecontent_comment"}


def test_comment_regist_success(app, db, id_token, new_data, post):
    token = id_token
    resp = app.post("/comment/regist?id=" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]


def test_comment_regist_no_comment(app, db, id_token, new_data, post):
    token = id_token
    del new_data["content"]
    resp = app.post("/comment/regist?id=" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
    assert not data["success"]


def test_comment_regist_empty_comment(app, db, id_token, new_data, post):
    token = id_token
    new_data["content"] = ""
    resp = app.post("/comment/regist?id=" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
    assert not data["success"]


def test_comment_regist_wrong_userid(app, db, id_token, new_data, post):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = app.post("/comment/regist?id=" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]


def test_comment_regist_wrong_postid(app, db, id_token, new_data, post):
    token = id_token
    resp = app.post("/comment/regist?id=" + str(post.id) + "a", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]
