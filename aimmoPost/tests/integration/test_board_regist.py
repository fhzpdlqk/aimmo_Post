import pytest
import json
import uuid


def test_board_regist_success(app, id_token):
    token = id_token
    resp = app.post("/board/regist", data=json.dumps({"boardname": "test_board_name"}), content_type="application/json", headers={"Token": token})
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))

    assert data["success"]


def test_board_regist_wrong_boardname(app, id_token):
    token = id_token
    resp = app.post("/board/regist", data=json.dumps({"board_name": "test_board_name"}), content_type="application/json", headers={"Token": token})
    assert resp.status_code == 400
    data = json.loads(resp.data.decode("utf-8"))

    assert not data["success"]
