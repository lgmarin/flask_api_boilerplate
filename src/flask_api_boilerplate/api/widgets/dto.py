import re
from datetime import date, datetime, timezone

from dateutil import parser
from flask_restx.inputs import URL
from flask_restx.reqparse import RequestParser

from flask_api_boilerplate.utils.datetime import make_tzaware, DATE_MONTH_NAME


def widget_name(name: str) -> str:
    """Validation method, allows for the string to contain letters, number, '-' and '_'."""

    if not re.compile(r"^[\w-]+$").match(name):
        raise ValueError(
            f"'{name}' contains one or more invalid characters. Widget name must have only letters, number, hyphen or underscore."
        )

    return name
