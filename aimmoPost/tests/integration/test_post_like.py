import pytest
import json
import uuid
from aimmoPost.tests.factory.post_factory import PostFactory


def test_post_like(app, db, id_token, post):
    token = id_token
    resp = app.post("/post/like/?id=" + str(post.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    temp = len(post.like)
    assert resp.status_code == 200
    assert data["success"]
    post.reload()
    assert len(post.like) - temp == 1
