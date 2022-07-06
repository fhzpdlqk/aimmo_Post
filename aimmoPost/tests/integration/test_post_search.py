import pytest
import json
import uuid

from aimmoPost.tests.factory.post_factory import PostFactory


def test_post_search_success(app, db, id_token, post, board):
    token = id_token
    PostFactory.create(board=board.id)
    resp = app.post("/post/search/" + str(board.id), data=json.dumps({"search_word": "title"}), content_type="application/json", headers={"Token": token})
    assert resp.status_code == 200
    data = json.loads(resp.data.decode("utf-8"))
    assert data["success"]
