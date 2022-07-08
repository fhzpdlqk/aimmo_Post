import pytest
import json
import uuid
from aimmoPost.tests.factory.recomment_factory import ReCommentFactory
from aimmoPost.tests.factory.user_factory import UserFactory
from aimmoPost.app.schemas.UserSchema import User


def test_recomment_like_success(app, db, id_token, recomment):
    token = id_token
    resp = app.post("/recomment/like/" + str(recomment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    temp = len(recomment.like)
    assert resp.status_code == 200
    assert data["success"]
    recomment.reload()
    assert len(recomment.like) - temp == 1


def test_recomment_like_cancel_success(app, db, id_token):
    token = id_token
    already_user = User.objects(user_id="testid")[0]
    recomment = ReCommentFactory.create(like=[already_user])
    resp = app.post("/recomment/like/" + str(recomment.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    temp = len(recomment.like)
    assert resp.status_code == 200
    assert data["success"]
    recomment.reload()
    assert len(recomment.like) - temp == -1


def test_recomment_like_no_commentid(app, db, id_token):
    token = id_token
    resp = app.post("/recomment/like/", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 404


def test_recomment_like_wrong_commentid(app, db, id_token, recomment):
    token = id_token
    resp = app.post("/recomment/like/" + str(recomment.id) + "a", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]


def test_comment_like_wrong_userid(app, db, id_token, recomment):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = app.post("/recomment/like/" + str(recomment.id) + "a", content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 401
    assert not data["success"]
