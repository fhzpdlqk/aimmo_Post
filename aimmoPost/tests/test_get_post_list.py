import aimmoPost.aimmoPost as ai
import pytest
import json


@pytest.fixture
def api():
    test_api = ai.app
    api = test_api.test_client()
    return api


def test_get_post_list_no_filter(api):
    resp = api.get("/post/list/?page=1", content_type="application/json")
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]
    for data in datas["message"]:
        assert isinstance(data["writer"], str) and len(data["writer"]) > 0
        assert isinstance(data["date"], str) and len(data["date"]) > 0
        assert isinstance(data["title"], str) and len(data["title"]) > 0
        assert isinstance(data["content"], str) and len(data["content"]) > 0
        assert isinstance(data["tag"], list)
        assert isinstance(data["notice"], bool)
        assert isinstance(data["comment"], list)
        assert isinstance(data["like"], list)


def test_get_post_list_success_filter_like(api):
    resp = api.get("/post/list/?page=1&filter=like", content_type="application/json")
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]
    for data in datas["message"]:
        assert isinstance(data["writer"], str) and len(data["writer"]) > 0
        assert isinstance(data["date"], str) and len(data["date"]) > 0
        assert isinstance(data["title"], str) and len(data["title"]) > 0
        assert isinstance(data["content"], str) and len(data["content"]) > 0
        assert isinstance(data["tag"], list)
        assert isinstance(data["notice"], bool)
        assert isinstance(data["comment"], list)
        assert isinstance(data["like"], list)


def test_get_post_list_success_filter_comment(api):
    resp = api.get("/post/list/?page=1&filter=comment", content_type="application/json")
    datas = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert datas["success"]
    for data in datas["message"]:
        assert isinstance(data["writer"], str) and len(data["writer"]) > 0
        assert isinstance(data["date"], str) and len(data["date"]) > 0
        assert isinstance(data["title"], str) and len(data["title"]) > 0
        assert isinstance(data["content"], str) and len(data["content"]) > 0
        assert isinstance(data["tag"], list)
        assert isinstance(data["notice"], bool)
        assert isinstance(data["comment"], list)
        assert isinstance(data["like"], list)


def test_get_post_list_pageover(api):
    resp = api.get("/post/list/?page=100", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"]
    assert len(data["message"]) == 0


def test_get_post_list_pagedown(api):
    resp = api.get("/post/list/?page=-1", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not data["success"]


def test_get_post_list_deferent_type(api):
    resp = api.get("/post/list/?page='abcd'", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not data["success"]


def test_get_post_list_not_parameter(api):
    resp = api.get("/post/list/", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not data["success"]


def test_get_post_list_filter_differ(api):
    resp = api.get("/post/list/?page=2&filter=nofilter", content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert not data["success"]
