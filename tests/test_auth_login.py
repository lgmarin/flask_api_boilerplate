from http import HTTPStatus

from flask_api_boilerplate.models.user import User
from tests.util import EMAIL, register_user, login_user


def test_login(client, db):
    register_user(client)

    response = login_user(client)

    assert response.status_code == HTTPStatus.OK
