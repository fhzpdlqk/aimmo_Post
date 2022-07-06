import pytest
import json
from aimmoPost.tests.factory.post_factory import PostFactory


def test_post_list_success_like(app, db, id_token, board):
    token = id_token
    resp = app.get(f"/post/list/{board.id}/1", content_type="application/json", headers={"Token": token})
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]
    for data in datas["message"]:
        assert isinstance(data["writer"], str) and len(data["writer"]) > 0
        assert isinstance(data["date"], str) and len(data["date"]) > 0
        assert isinstance(data["title"], str) and len(data["title"]) > 0
        assert isinstance(data["tag"], list)
        assert isinstance(data["notice"], bool)
        assert isinstance(data["num_like"], int)
        assert isinstance(data["num_comment"], int)
        assert isinstance(data["is_like"], bool)


def test_post_list_negative_page(app, db, id_token, board):
    token = id_token
    resp = app.get(f"/post/list/{board.id}/-1", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
    assert not data["success"]


def test_post_list_big_page(app, db, id_token, board):
    token = id_token
    resp = app.get(f"/post/list/{board.id}/1000", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]
    assert data["message"] == []


def test_post_list_not_page(app, db, id_token, board):
    token = id_token
    resp = app.get(f"/post/list/{board.id}/", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 404
