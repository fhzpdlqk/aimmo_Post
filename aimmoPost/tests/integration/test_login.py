import pytest
import json


def test_login_success(app, db):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = app.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert isinstance(data["token"], str)


def test_login_no_id(app, db):
    login_data = {"user_pw": "testpw"}
    resp = app.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    assert resp.status_code == 401


def test_login_no_pw(app, db):
    login_data = {"user_id": "testid"}
    resp = app.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    assert resp.status_code == 401


def test_login_wrong_id(app, db):
    login_data = {"user_id": "testid1", "user_pw": "testpw"}
    resp = app.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    assert resp.status_code == 401


def test_login_wrong_pw(app, db):
    login_data = {"user_id": "testid", "user_pw": "testpw11"}
    resp = app.post("/user/login", data=json.dumps(login_data), content_type="application/json")
    assert resp.status_code == 401
