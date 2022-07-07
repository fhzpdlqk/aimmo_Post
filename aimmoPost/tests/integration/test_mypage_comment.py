import pytest
import json
import uuid


def test_mypage_comment_success(app, id_token):
    token = id_token
    resp = app.get("/mypage/comment", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))

    assert data["success"]
    assert isinstance(data["message"], list)


def test_mypage_comment_invalid_token(app, id_token):
    token = id_token + "a"
    resp = app.get("/mypage/comment", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 401
    data = json.loads(resp.data.decode("utf-8"))

    assert not data["success"]
