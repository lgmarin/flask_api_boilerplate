from flask import Blueprint
from flask_restx import Api

from flask_api_boilerplate.api.auth.endpoints import auth_namespace
from flask_api_boilerplate.api.widgets.endpoints import widget_namespace

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_blueprint,
    version="1.0",
    title="Flask API with JWT Auth",
    description="Flask API Boilerplate with flask-restx and jwt auth.",
    doc="/ui",
    authorizations=authorizations,
)

api.add_namespace(auth_namespace, path="/auth")
api.add_namespace(widget_namespace, path="/widgets")
