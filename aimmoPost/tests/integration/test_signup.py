import pytest
import json
from aimmoPost.app.schemas.UserSchema import User


def test_signup_success(app, db):
    login_data = {"user_id": "test_make_id", "user_pw": "testpw"}
    resp = app.post("/user/", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    User.objects(user_id="test_make_id").delete()


def test_signup_duplicate_id(app, db):
    login_data = {"user_id": "testid", "user_pw": "testpw"}
    resp = app.post("/user/", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 409


def test_signup_no_id(app, db):
    login_data = {"user_pw": "testpw"}
    resp = app.post("/user/", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400


def test_signup_no_pw(app, db):
    login_data = {"user_id": "testid"}
    resp = app.post("/user/", data=json.dumps(login_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
