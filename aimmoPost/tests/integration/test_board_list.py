import pytest
import json
import uuid


def test_board_regist_success(app, id_token):
    token = id_token
    resp = app.get("/board/list", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))

    assert data["success"]
    assert isinstance(data["message"], list)
