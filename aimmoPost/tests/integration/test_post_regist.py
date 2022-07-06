import pytest
import json
import uuid


@pytest.fixture
def new_data():
    return {"title": "post_title", "content": "post_content", "tag": ["tag_1", "tag_2"], "notice": True}


def test_post_regist_success(app, db, id_token, new_data, board):
    token = id_token
    resp = app.post("/post/regist/" + str(board.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"success": True}


def test_post_regist_wrong_id(app, db, id_token, new_data, board):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    print(token)
    resp = app.post("/post/regist/" + str(board.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401


def test_post_regist_no_title(app, db, id_token, new_data, board):
    token = id_token
    new_data["title"] = ""
    resp = app.post("/post/regist/" + str(board.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400


def test_post_regist_no_content(app, db, id_token, new_data, board):
    token = id_token
    new_data["content"] = ""
    resp = app.post("/post/regist/" + str(board.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400


def test_post_regist_no_notice(app, db, id_token, new_data, board):
    token = id_token
    new_data["notice"] = ""
    resp = app.post("/post/regist/" + str(board.id), data=json.dumps(new_data), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
