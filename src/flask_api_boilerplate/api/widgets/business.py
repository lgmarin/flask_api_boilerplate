from http import HTTPStatus
from flask import jsonify, url_for, Response
from flask_restx import abort

from flask_api_boilerplate import db
from flask_api_boilerplate.models.user import User
from flask_api_boilerplate.models.widget import Widget
from flask_api_boilerplate.api.auth.decorators import admin_required


@admin_required
def create_widget(widget_dict: dict) -> Response:
    name = widget_dict["name"]

    if Widget.find_by_name(name=name):
        error = f"Widget name: {name} already exists. It must be unique."
        abort(HTTPStatus.CONFLICT, error, status="fail")

    widget = Widget(**widget_dict)
    owner = User.find_by_public_id(create_widget.public_id)
    widget.owner_id = owner.id
    db.session.add(widget)
    db.session.commit()

    response = jsonify(status="success", message=f"New widget added: {name}.")
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for("api.widget", name=name)

    return response
