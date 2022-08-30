from flask_api_boilerplate import db
from flask_api_boilerplate.utils import utc_now


class Widget(db.Model):
    """Widget Model for the API"""

    __tablename__ = "widget"

    id = db.Column(db.Integer, primary_key=True, autoicrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    info_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=utc_now)
    dadline = db.Column(db.DateTime)
