from flask import url_for

EMAIL = "testuser@testmail.com"
PASSWORD = "123456789"
BAD_REQUEST = "Input payload validation failed"


def register_user(test_client, email=EMAIL, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_register"),
        data=f"email={email}&password={password}",
        content_type="application/x-www-form-urlencoded",
    )


def login_user(test_client, email=EMAIL, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_login"),
        data={"email": f"{email}", "password": f"{password}"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def get_user(test_client, access_token):
    return test_client.get(
        url_for("api.auth_user"), headers={"Authorization": f"Bearer {access_token}"}
    )
