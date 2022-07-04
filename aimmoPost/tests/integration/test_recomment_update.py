import pytest
import json
import uuid


@pytest.fixture
def new_data():
    return {"content": "recoment_content_update"}


def test_recomment_update_success(app, db, id_token, new_data, recomment):
    token = id_token
    resp = app.put("/recomment/?recomment_id=" + str(recomment.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]
    recomment.reload()
    assert recomment.content == "recoment_content_update"


def test_recomment_update_wrong_userid(app, db, id_token, new_data, recomment):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = app.put("/recomment/?recomment_id=" + str(recomment.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]


def test_recomment_update_def_userid(app, db, wrong_id_token, new_data, recomment):
    token = wrong_id_token
    resp = app.put("/recomment/?recomment_id=" + str(recomment.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]


def test_recomment_update_wrong_commentid(app, db, id_token, new_data, recomment):
    token = id_token
    resp = app.put("/recomment/?recomment_id=" + str(recomment.id) + "a", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]


def test_recomment_update_no_commentid(app, db, id_token, new_data, recomment):
    token = id_token
    resp = app.put("/recomment/", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
    assert not data["success"]


def test_recomment_update_empty_content(app, db, id_token, new_data, recomment):
    token = id_token
    new_data["content"] = ""
    resp = app.put("/recomment/?recomment_id=" + str(recomment.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
    assert not data["success"]


def test_recomment_update_no_content(app, db, id_token, new_data, recomment):
    token = id_token
    del new_data["content"]
    resp = app.put("/recomment/?recomment_id=" + str(recomment.id) + "a", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
    assert not data["success"]
