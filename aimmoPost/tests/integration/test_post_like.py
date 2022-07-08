import pytest
import json
import uuid
from aimmoPost.tests.factory.post_factory import PostFactory
from aimmoPost.tests.factory.user_factory import UserFactory
from aimmoPost.app.schemas.UserSchema import User


def test_post_like_success(app, db, id_token, post):
    token = id_token
    resp = app.post("/post/like/" + str(post.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    temp = len(post.like)
    assert resp.status_code == 200
    assert data["success"]
    post.reload()
    assert len(post.like) - temp == 1


def test_post_like_cancel_success(app, db, id_token):
    token = id_token
    already_user = User.objects(user_id="testid")[0]
    post = PostFactory.create(like=[already_user])
    resp = app.post("/post/like/" + str(post.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    temp = len(post.like)
    assert resp.status_code == 200
    assert data["success"]
    post.reload()
    assert len(post.like) - temp == -1


def test_post_like_no_postid(app, db, id_token):
    token = id_token
    resp = app.post("/post/like/", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 404


def test_post_like_wrong_postid(app, db, id_token, post):
    token = id_token
    resp = app.post("/post/like/" + str(post.id) + "a", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]


def test_post_like_wrong_userid(app, db, id_token, post):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = app.post("/post/like/" + str(post.id) + "a", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]
