from http import HTTPStatus
from flask_restx import Namespace, Resource

from flask_api_boilerplate.api.widgets.dto import widget_req_parser
from flask_api_boilerplate.api.widgets.business import create_widget

widget_namespace = Namespace(name="widgets", validate=True)


@widget_namespace.route("", endpoint="widget_list")
@widget_namespace.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@widget_namespace.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@widget_namespace.response(
    int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
)
class WidgetList(Resource):
    """Handles HTTP requests to URL: /widgets"""

    @widget_namespace.doc(security="Bearer")
    @widget_namespace.response(int(HTTPStatus.CREATED), "Added new widget.")
    @widget_namespace.response(int(HTTPStatus.FORBIDDEN), "Admnistrator token required.")
    @widget_namespace.response(int(HTTPStatus.CONFLICT), "Widget name already exists.")
    @widget_namespace.expect(widget_req_parser)
    def post(self):
        """Create a widget."""

        widget_dict = widget_req_parser.parse_args()
        return create_widget(widget_dict)
