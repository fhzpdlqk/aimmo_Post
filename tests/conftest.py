import pytest
import mongoengine as me
from flask import current_app

@pytest.fixture(scope="session", autouse=True)
def app():
    from app import create_app
    app = create_app("test")
    return app


@pytest.fixture(scope="function", autouse=True)
def db(app):
    me.connect(host=current_app.config["MONGODB_URI"])
    yield db
    me.disconnect()
