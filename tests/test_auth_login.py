from http import HTTPStatus

from flask_api_boilerplate.models.user import User
from tests.util import EMAIL, PASSWORD, BAD_REQUEST, register_user, login_user

SUCCESS = "successfully registered"
EMAIL_ALREADY_EXISTS = f"{EMAIL} already in use!"


def test_login(client, db):
    register_user(client)

    response = login_user(client)

    assert response.status_code == HTTPStatus.OK


def test_auth_user(client, db):
    response = register_user(client, email=EMAIL, password=PASSWORD)

    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS
    assert "token_type" in response.json and response.json["token_type"] == "bearer"
    assert "expires_in" in response.json and response.json["expires_in"] == 5
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    result = User.decode_access_token(access_token)
    assert result.success

    user_dict = result.value
    assert not user_dict["admin"]

    user = User.find_by_public_id(user_dict["public_id"])
    assert user and user.email == EMAIL


def test_auth_register_invalid_email(client):
    invalid_email = "first last"

    response = register_user(client, email=invalid_email, password=PASSWORD)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "message" in response.json and response.json["message"] == BAD_REQUEST
    assert "token_type" not in response.json
    assert "expires_in" not in response.json
    assert "access_token" not in response.json
    assert "errors" in response.json
    assert "password" not in response.json["errors"]
    assert "email" in response.json["errors"]
    assert response.json["errors"]["email"] == f"{invalid_email} is not a valid email"
