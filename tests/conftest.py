import pytest

from flask_api_boilerplate import create_app
from flask_api_boilerplate import db as database
from flask_api_boilerplate.models.user import User
from tests.util import EMAIL, PASSWORD


@pytest.fixture
def app():
    app = create_app("testing")
    return app


@pytest.fixture
def db(app, client, request):
    database.drop_all()
    database.create_all()
    database.session.commit()

    def close():
        database.session.remove()

    request.addfinalizer(close)
    return database


@pytest.fixture
def user(db):
    user = User(email=EMAIL, password=PASSWORD)
    db.session.add(user)
    db.session.commit()

    return user
