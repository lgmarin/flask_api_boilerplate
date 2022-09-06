from http import HTTPStatus
from flask import jsonify, url_for, Response
from flask_restx import abort, marshal
from flask_sqlalchemy import Pagination

from flask_api_boilerplate import db
from flask_api_boilerplate.models.user import User
from flask_api_boilerplate.models.widget import Widget
from flask_api_boilerplate.api.auth.decorators import admin_required, token_required
from flask_api_boilerplate.api.widgets.dto import pagination_model, widget_name


@admin_required
def create_widget(widget_dict: dict) -> Response:
    """Create a new widget

    Args:
        widget_dict (dict): Dict containing new widget data

    Returns:
        Response: HTTP Response
    """
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


@token_required
def retrieve_widget_list(page: int, per_page: int) -> Response:
    """Retrieve a list of widgets with pagination

    Args:
        page (int): Page number
        per_page (int): Number of intems per page

    Returns:
        Response: HTTP Response containing the JSON data
    """
    pagination = Widget.query.paginate(page, per_page, error_out=False)
    response_data = marshal(pagination, pagination_model)
    response_data["links"] = _pagination_nav_links(pagination)

    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination)
    response.headers["Total-Count"] = pagination.total

    return response


@token_required
def retrieve_widget(name: str) -> Response:
    """Retrieve a single widget based on it's name.

    Args:
        name (str): Widget name

    Returns:
        Response: HTTP Response containing JSON object
    """
    return Widget.query.filter_by(
        name=name.lower().first_or_404(description=f"{name} not found in database.")
    )


@admin_required
def delete_widget(name: str) -> Response:
    """Delete a single object by name

    Args:
        name (str): Widget name

    Returns:
        Response: HTTP Response containing JSON object
    """
    widget = Widget.query.filter_by(name=name.lower()).first_or_404(
        description=f"{name} not found in database."
    )
    db.session.delete(widget)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT


@token_required
def update_widget(name: str, widget_dict: dict) -> Response:
    """Update Widget by the provided name

    Args:
        name (str): Widget name
        widget_dict (dict): Widget dict containing the new data to update

    Returns:
        Response: HTTP Response containing JSON object
    """
    widget = Widget.query.find_by_name(name.lower())

    if widget:
        for k, v in widget_dict.items():
            setattr(widget, k, v)

        db.session.commit()
        message = f"'{name}' was successfully updated!"
        response_dict = dict(status="success", message=message)

        return response_dict, HTTPStatus.OK

    try:
        valid_name = widget_name(name.lower())
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e), status="fail")

    widget_dict["name"] = valid_name

    return create_widget(widget_dict)


# Private Methods
def _pagination_nav_links(pagination: Pagination) -> dict:
    """Generate navigation links for the pagination response

    Args:
        pagination (Pagination): Pagination object to process

    Returns:
        dict: Navigation links to merge into HTTP response
    """
    nav_links = {}

    per_page = pagination.per_page
    this_page = pagination.page
    last_page = pagination.pages
    nav_links["self"] = url_for("api.widget_list", page=this_page, per_page=per_page)
    nav_links["first"] = url_for("api.widget_list", page=1, per_page=per_page)

    if pagination.has_prev:
        nav_links["prev"] = url_for(
            "api.wiget_list", page=this_page - 1, per_page=per_page
        )

    if pagination.has_next:
        nav_links["next"] = url_for(
            "api.widget_list", page=this_page + 1, per_page=per_page
        )

    nav_links["last"] = url_for("api.widget_list", page=last_page, per_page=per_page)

    return nav_links


def _pagination_nav_header_links(pagination: Pagination) -> str:
    """Generate navigation headers for the pagination response

    Args:
        pagination (Pagination): Pagination object to process

    Returns:
        str: String containing the headers to merge into HTTP response
    """
    url_dict = _pagination_nav_links(pagination)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f'<{url}>; rel="{rel}", '
    return link_header.strip().strip(",")
