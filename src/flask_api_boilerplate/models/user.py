from datetime import datetime, timezone
from uuid import uuid4
from flask import current_app

from flask_api_boilerplate import db, bcrypt


class User(db.Model):
    """Contains User information and login credentials"""

    __tablename__ = "app_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=utc_now)
    admin = db.Column(db.Boolean, default=False)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))
