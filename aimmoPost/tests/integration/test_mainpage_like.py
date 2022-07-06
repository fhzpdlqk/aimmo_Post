import pytest
import json
import uuid


def test_mainpage_like_success(app, id_token):
    token = id_token
    resp = app.get("/mainpage/like", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))

    assert data["success"]
    assert isinstance(data["message"], list)
    for index in range(1, len(data["message"])):
        assert data["message"][index]["num_like"] <= data["message"][index - 1]["num_like"]
