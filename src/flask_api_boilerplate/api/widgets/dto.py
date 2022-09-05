import re
from datetime import date, datetime, timezone, time

from dateutil import parser
from flask_restx.inputs import URL, positive
from flask_restx.reqparse import RequestParser

from flask_api_boilerplate.utils.datetime import make_tzaware, DATE_MONTH_NAME


def widget_name(name: str) -> str:
    """Validation method, allows for the string to contain letters, number, '-' and '_'."""

    if not re.compile(r"^[\w-]+$").match(name):
        raise ValueError(
            f"'{name}' contains one or more invalid characters. Widget name must have only letters, number, hyphen or "
            "underscore."
        )

    return name


def future_date_from_string(date_str: str):
    """Validation method for a date stored and formatted as a string."""

    try:
        parsed_date = parser.parse(date_str)
    except ValueError:
        raise ValueError(
            f"Failed to parse '{date_str}' as a valid date. Make sure to use '2018-5-13' -or- '05/13/2018' -or- 'May "
            "13 2018'."
        )

    if parsed_date.date() < date.today():
        raise ValueError(
            f"The date {parsed_date.strftime(DATE_MONTH_NAME)} is older than "
            f"{datetime.now().strftime(DATE_MONTH_NAME)}. You must enter a date in the future."
        )

    deadline = datetime.combine(parsed_date.date(), time.max)
    deadline_utc = make_tzaware(deadline, use_tz=timezone.utc)

    return deadline_utc


# Parser
widget_req_parser = RequestParser(bundle_errors=True)
widget_req_parser.add_argument(
    "name",
    type=widget_name,
    location="form",
    required=True,
    nullable=False,
    case_sensitive=True,
)

widget_req_parser.add_argument(
    "info_url",
    type=URL(schemes=["http", "https"]),
    location="form",
    required=True,
    nullable=False,
)

widget_req_parser.add_argument(
    "deadline",
    type=future_date_from_string,
    location="form",
    required=True,
    nullable=False,
)


pagination_req_parser = RequestParser(bundle_errors=True)
pagination_req_parser.add_argument("page", type=positive, required=False, default=1)
pagination_req_parser.add_argument(
    "per_page", type=positive, required=False, default=10, choices=[5, 10, 25, 50]
)
