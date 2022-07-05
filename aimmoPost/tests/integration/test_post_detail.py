import pytest
import json


def test_post_detail_success(app, db, id_token, post):
    token = id_token
    resp = app.get("/post/?id=" + str(post.id), content_type="application/json", headers={"Token": token})

    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data["success"] == True
    data = data["message"]
    assert isinstance(data["writer"], str) and len(data["writer"]) > 0
    assert isinstance(data["date"], str) and len(data["date"]) > 0
    assert isinstance(data["title"], str) and len(data["title"]) > 0
    assert isinstance(data["content"], str) and len(data["content"]) > 0
    assert isinstance(data["tag"], list)
    assert isinstance(data["notice"], bool)
    assert isinstance(data["comment"], list)
    assert isinstance(data["is_like"], bool)
    for i in data["comment"]:
        assert isinstance(i["writer"], str) and len(i["writer"]) > 0
        assert isinstance(i["date"], str) and len(i["date"]) > 0
        assert isinstance(i["content"], str) and len(i["content"]) > 0
        assert isinstance(i["recomment"], list)
        assert isinstance(i["is_like"], bool)
        for j in i["recomment"]:
            assert isinstance(j["writer"], str) and len(j["writer"]) > 0
            assert isinstance(j["date"], str) and len(j["date"]) > 0
            assert isinstance(j["content"], str) and len(j["content"]) > 0
            assert isinstance(j["is_like"], bool)


def test_post_detail_wrongid(app, db, id_token, post):
    token = id_token
    resp = app.get("/post/?id=" + str(post.id) + "a", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]
