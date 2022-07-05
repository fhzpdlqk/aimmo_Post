import pytest
import json
import uuid


@pytest.fixture
def new_data():
    return {"title": "sampletitle_update", "content": "samplecontent_update", "tag": ["st_1_update", "st_2_update"], "notice": False}


def test_post_update_success(app, db, id_token, post, new_data):
    token = id_token
    resp = app.put("/post/" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"success": True}
    post.reload()
    assert post.title == "sampletitle_update"
    assert post.content == "samplecontent_update"
    assert post.tag == ["st_1_update", "st_2_update"]
    assert post.notice == False


def test_post_update_notitle(app, db, id_token, post, new_data):
    token = id_token
    new_data["title"] = ""
    resp = app.put("/post/" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"success": True}
    post.reload()
    assert post.title == "sampletitle"
    assert post.content == "samplecontent_update"
    assert post.tag == ["st_1_update", "st_2_update"]
    assert post.notice == False


def test_post_update_nocontent(app, db, id_token, post, new_data):
    token = id_token
    new_data["content"] = ""
    resp = app.put("/post/" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"success": True}
    post.reload()
    assert post.title == "sampletitle_update"
    assert post.content == "samplecontent"
    assert post.tag == ["st_1_update", "st_2_update"]
    assert post.notice == False


def test_post_update_nonotice(app, db, id_token, post, new_data):
    token = id_token
    del new_data["notice"]
    resp = app.put("/post/" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"success": True}
    post.reload()
    assert post.title == "sampletitle_update"
    assert post.content == "samplecontent_update"
    assert post.tag == ["st_1_update", "st_2_update"]
    assert post.notice == True


def test_post_update_wrong_userid(app, db, id_token, post, new_data):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = app.put("/post/" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert data["success"] == False


def test_post_update_wrong_id(app, db, id_token, post, new_data):
    token = id_token
    resp = app.put("/post/" + str(post.id) + "a", data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert data["success"] == False


def test_post_update_wrong_def_user(app, db, wrong_id_token, post, new_data):
    token = wrong_id_token
    resp = app.put("/post/" + str(post.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert data["success"] == False
