from http import HTTPStatus
import time
from flask import url_for

from tests.util import EMAIL, get_user, register_user, login_user


def test_auth_get_user(client, db):
    register_user(client)
    response = login_user(client)

    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = get_user(client, access_token)

    assert response.status_code == HTTPStatus.OK
    assert "email" in response.json and response.json["email"] == EMAIL
    assert "admin" in response.json and not response.json["admin"]
