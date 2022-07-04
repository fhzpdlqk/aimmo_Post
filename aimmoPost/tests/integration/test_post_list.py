import pytest
import json
from aimmoPost.tests.factory.post_factory import PostFactory


def test_post_list_success_like(app, db, id_token):
    resp = app.get("/post/list/?page=1&filter=like", content_type="application/json")
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


def test_post_list_success_comment(app, db, id_token):
    resp = app.get("/post/list/?page=1&filter=comment", content_type="application/json")
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


def test_post_list_success_date(app, db, id_token):
    resp = app.get("/post/list/?page=1&filter=date", content_type="application/json")
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


def test_post_list_success_no_filter(app, db, id_token):
    resp = app.get("/post/list/?page=1", content_type="application/json")
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


def test_post_list_negative_page(app, db, id_token):
    resp = app.get("/post/list/?page=-1", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
    assert not data["success"]


def test_post_list_big_page(app, db, id_token):
    resp = app.get("/post/list/?page=1000", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]
    assert data["message"] == []


def test_post_list_not_page(app, db, id_token):
    resp = app.get("/post/list/", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]


def test_post_list_wrong_filter(app, db, id_token):
    resp = app.get("/post/list/?filter=nofilter", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]
