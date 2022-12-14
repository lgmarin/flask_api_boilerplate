from http import HTTPStatus
from flask_restx import Namespace, Resource

from flask_api_boilerplate.api.widgets.dto import (
    widget_req_parser,
    pagination_req_parser,
    widget_owner_model,
    widget_model,
    pagination_links_model,
    pagination_model,
)
from flask_api_boilerplate.api.widgets.business import (
    create_widget,
    retrieve_widget_list,
    retrieve_widget,
    delete_widget,
)


widget_namespace = Namespace(name="widgets", validate=True)
widget_namespace.models[widget_owner_model.name] = widget_owner_model
widget_namespace.models[widget_model.name] = widget_model
widget_namespace.models[pagination_links_model.name] = pagination_links_model
widget_namespace.models[pagination_model.name] = pagination_model


@widget_namespace.route("", endpoint="widget_list")
@widget_namespace.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@widget_namespace.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@widget_namespace.response(
    int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
)
class Widgets(Resource):
    """Handles HTTP requests to URL: /widgets"""

    @widget_namespace.doc(security="Bearer")
    @widget_namespace.response(
        int(HTTPStatus.OK), "Retrieve widget list.", pagination_model
    )
    @widget_namespace.expect(pagination_req_parser)
    def get(self):
        """Retrieve a list of widgets."""

        request_data = pagination_req_parser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")

        return retrieve_widget_list(page, per_page)

    @widget_namespace.doc(security="Bearer")
    @widget_namespace.response(int(HTTPStatus.CREATED), "Added new widget.")
    @widget_namespace.response(int(HTTPStatus.FORBIDDEN), "Admnistrator token required.")
    @widget_namespace.response(int(HTTPStatus.CONFLICT), "Widget name already exists.")
    @widget_namespace.expect(widget_req_parser)
    def post(self):
        """Create a widget."""

        widget_dict = widget_req_parser.parse_args()
        return create_widget(widget_dict)


@widget_namespace.route("/<name>", endpoint="widget")
@widget_namespace.param("name", "Widget name")
@widget_namespace.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@widget_namespace.response(int(HTTPStatus.NOT_FOUND), "Widget not found.")
@widget_namespace.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@widget_namespace.response(
    int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
)
class Widget(Resource):
    """Handles HTTP request to URL: /widgets/{name}"""

    @widget_namespace.doc(security="Bearer")
    @widget_namespace.response(int(HTTPStatus.OK), "Retrieved widget.", widget_model)
    @widget_namespace.marshal_with(widget_model)
    def get(self, name: str):
        """Retrieve a single widget by it's name."""

        return retrieve_widget(name)

    @widget_namespace.doc(security="Bearer")
    @widget_namespace.response(int(HTTPStatus.NO_CONTENT), "Widget deleted.")
    @widget_namespace.response(
        int(HTTPStatus.FORBIDDEN), "Administrator token required."
    )
    def delete(self, name: str):
        """Delete a widget by it's name."""

        return delete_widget(name)
