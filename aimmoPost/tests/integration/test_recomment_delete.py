import pytest
import json
import uuid


def test_recomment_delete_success(app, db, id_token, recomment):
    token = id_token
    resp = app.delete("/recomment/?recomment_id=" + str(recomment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]


def test_recomment_delete_wrong_userid(app, db, id_token, recomment):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = app.delete("/recomment/?recomment_id=" + str(recomment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]


def test_recomment_delete_def_userid(app, db, wrong_id_token, recomment):
    token = wrong_id_token
    resp = app.delete("/recomment/?recomment_id=" + str(recomment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]


def test_recomment_delete_wrong_commentid(app, db, id_token, recomment):
    token = id_token
    resp = app.delete("/recomment/?recomment_id=" + str(recomment.id) + "a", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]


def test_recomment_delete_no_commentid(app, db, id_token, recomment):
    token = id_token
    resp = app.delete("/recomment/", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
    assert not data["success"]
