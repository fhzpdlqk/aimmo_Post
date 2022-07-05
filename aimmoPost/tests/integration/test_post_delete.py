import pytest
import json
import uuid


def test_post_delete_success(app, db, id_token, post):
    token = id_token
    resp = app.delete("/post/" + str(post.id), content_type="application/json", headers={"Token": token})
    print(resp.status_code)
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"success": True}


def test_post_delete_no_postid(app, db, id_token, post):
    token = id_token
    resp = app.delete("/post/", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 404


def test_post_delete_wrong_postid(app, db, id_token, post):
    token = id_token
    resp = app.delete("/post/" + str(post.id) + "A", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]


def test_post_delete_wrong_userid(app, db, id_token, post):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = app.delete("/post/" + str(post.id) + "A", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 401


def test_post_delete_wrong_def_user(app, db, wrong_id_token, post):
    token = wrong_id_token
    resp = app.delete("/post/" + str(post.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert data["success"] == False
