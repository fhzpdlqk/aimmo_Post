import pytest
import json
import uuid


def test_mainpage_recent_success(app, id_token):
    token = id_token
    resp = app.get("/mainpage/recent", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))

    assert data["success"]
    assert isinstance(data["message"], list)
    for index in range(1, len(data["message"])):
        assert data["message"][index]["date"] < data["message"][index - 1]["date"]
