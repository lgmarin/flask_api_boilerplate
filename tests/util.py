from flask import url_for

EMAIL = "testuser@testmail.com"
PASSWORD = "teste123"


def register_user(test_client, email=EMAIL, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_register"),
        data=f"email={email}&password={password}",
        content_type="application/x-www-from-urlencoded",
    )
