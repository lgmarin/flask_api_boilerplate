from http import HTTPStatus

from flask import current_app, jsonify
from flask_restx import abort

from flask_api_boilerplate import db
from flask_api_boilerplate.models.user import User


def process_registration_request(email: str, password: str):
    if User.find_by_email(email):
        abort(HTTPStatus.CONFLICT, f"{email} already in use!", status="fail")

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    access_token = new_user.encode_access_token()

    return _successful_response(
        token=access_token,
        status_code=HTTPStatus.CREATED,
        message="successfully registered",
    )


def _get_token_expire_time():
    token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
    token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    expires_in_seconds = token_age_h * 3600 + token_age_m * 60

    return expires_in_seconds if not current_app.config["TESTING"] else 5


def _successful_response(token: str, status_code: int, message: str):
    response = jsonify(
        status="success",
        message=message,
        access_token=token,
        token_type="bearer",
        expires_in=_get_token_expire_time(),
    )

    response.status_code = status_code
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"

    return response
