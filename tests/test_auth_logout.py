from http import HTTPStatus

from flask_api_boilerplate.models.token_blacklist import BlacklistedToken
from tests.util import register_user, login_user, logout_user

LOGOUT_SUCCESS = "successfully logged out."


def test_logout(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    blacklist = BlacklistedToken.query.all()
    assert len(blacklist) == 0
    response = logout_user(client, access_token)
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == LOGOUT_SUCCESS
    blacklist = BlacklistedToken.query.all()
    assert len(blacklist) == 1
    assert access_token == blacklist[0].token
