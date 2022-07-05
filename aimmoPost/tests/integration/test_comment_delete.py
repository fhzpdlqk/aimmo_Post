import pytest
import json
import uuid


def test_comment_delete_success(app, db, id_token, comment):
    token = id_token
    resp = app.delete("/comment/" + str(comment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]


def test_comment_delete_wrong_userid(app, db, id_token, comment):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = app.delete("/comment/" + str(comment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]


def test_comment_delete_def_userid(app, db, wrong_id_token, comment):
    token = wrong_id_token
    resp = app.delete("/comment/" + str(comment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]


def test_comment_delete_wrong_commentid(app, db, id_token, comment):
    token = id_token
    resp = app.delete("/comment/" + str(comment.id) + "a", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]


def test_comment_delete_no_commentid(app, db, id_token, comment):
    token = id_token
    resp = app.delete("/comment/", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 404
