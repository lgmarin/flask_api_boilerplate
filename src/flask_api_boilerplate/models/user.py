from datetime import datetime, timezone
from uuid import uuid4

from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from flask_api_boilerplate import db, bcrypt
from flask_api_boilerplate.utils.datetime import (
    utc_now,
    get_local_utcoffset,
    make_tzaware,
    localized_dt_string,
)


class User(db.Model):
    """Contains User information and login credentials"""

    __tablename__ = "app_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=utc_now)
    admin = db.Column(db.Boolean, default=False)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))

    def __repr__(self) -> str:
        return (
            f"<User email={self.email}, public_id={self.public_id}, admin={self.admin}"
        )

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password: str):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.password_hash = hash_bytes.decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    @hybrid_property
    def registered_on_str(self) -> str:
        registered_on_utc = make_tzaware(
            self.registered_on, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(registered_on_utc, use_tz=get_local_utcoffset())
