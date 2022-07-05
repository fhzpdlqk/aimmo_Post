import pytest
import json
import uuid
from aimmoPost.tests.factory.comment_factory import CommentFactory
from aimmoPost.tests.factory.user_factory import UserFactory
from aimmoPost.aimmoPost.models.User import User


def test_comment_like_success(app, db, id_token, comment):
    token = id_token
    resp = app.post("/comment/like/?comment_id=" + str(comment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    temp = len(comment.like)
    assert resp.status_code == 200
    assert data["success"]
    comment.reload()
    assert len(comment.like) - temp == 1


def test_comment_like_cancel_success(app, db, id_token):
    token = id_token
    already_user = User.objects(user_id="testid")[0]
    comment = CommentFactory.create(like=[already_user])
    resp = app.post("/comment/like/?comment_id=" + str(comment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    temp = len(comment.like)
    assert resp.status_code == 200
    assert data["success"]
    comment.reload()
    assert len(comment.like) - temp == -1


def test_comment_like_no_commentid(app, db, id_token):
    token = id_token
    resp = app.post("/comment/like/", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 400
    assert not data["success"]


def test_comment_like_wrong_commentid(app, db, id_token, comment):
    token = id_token
    resp = app.post("/comment/like/?comment_id=" + str(comment.id) + "a", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]


def test_comment_like_wrong_userid(app, db, id_token, comment):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = app.post("/comment/like/?comment_id=" + str(comment.id) + "a", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]
