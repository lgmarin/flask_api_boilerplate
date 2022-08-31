from http import HTTPStatus

from flask_restx import Namespace, Resource

from flask_api_boilerplate.api.auth.dto import auth_req_parser
from flask_api_boilerplate.api.auth.business import (
    process_registration_request,
    process_login_request,
)

auth_namespace = Namespace(
    name="auth",
    validate=True,
)


@auth_namespace.route("/register", endpoint="auth_register")
class RegisterUser(Resource):
    """Handles HTTP Requests to /api/v1/auth/register"""

    @auth_namespace.expect(auth_req_parser)
    @auth_namespace.response(int(HTTPStatus.CREATED), "New user successfully created!")
    @auth_namespace.response(
        int(HTTPStatus.CONFLICT), "Email address is already in use!"
    )
    @auth_namespace.response(int(HTTPStatus.BAD_REQUEST), "Validation Error!")
    @auth_namespace.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Something went wrong with the server."
    )
    def post(self):
        """Register a new user and return a valid Access Token"""

        request_data = auth_req_parser.parse_args()

        email = request_data.get("email")
        password = request_data.get("password")

        return process_registration_request(email, password)


@auth_namespace.route("/login", endpoint="login_user")
class LoginUser(Resource):
    """Handles HTTP Requests to /api/v1/auth/login"""

    @auth_namespace.expect(auth_req_parser)
    @auth_namespace.response(int(HTTPStatus.OK), "User logged in successfully!")
    @auth_namespace.response(
        int(HTTPStatus.UNAUTHORIZED), "emails or password does not match!"
    )
    @auth_namespace.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_namespace.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Something went wrong with the server."
    )
    def post(self):
        """Authenticate an existing user and return a valid access token."""

        request_data = auth_req_parser.parse_args()
        email = request_data.get("email")
        password = request_data.get("password")

        return process_login_request(email, password)
