from datetime import timezone, datetime, timedelta
from uuid import uuid4

from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
import jwt

from flask_api_boilerplate import db, bcrypt
from flask_api_boilerplate.utils.result import Result
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

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_public_id(cls, public_id: str):
        return cls.query.filter_by(public_id=public_id).first()

    def encode_access_token(self):
        now = datetime.now(timezone.utc)

        token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
        token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")

        expires_at = now + timedelta(hours=token_age_h, minutes=token_age_m)

        if current_app.config["TESTING"]:
            expires_at = now + timedelta(seconds=5)

        payload = dict(exp=expires_at, iat=now, sub=self.public_id, admin=self.admin)
        key = current_app.config.get("SECRET_KEY")

        return jwt.encode(payload, key, algorithm="HS256")

    @staticmethod
    def decode_access_token(access_token: str) -> Result:
        if isinstance(access_token, bytes):
            access_token = access_token.decode("ascii")

        if access_token.startswith("Bearer "):
            split = access_token.split("Bearer ")
            access_token = split[1].strip()

        try:
            key = current_app.config.get("SECRET_KEY")
            payload = jwt.decode(access_token, key, algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            error = "Access token expired. Login again to renew."
            return Result.Fail(error)

        except jwt.InvalidTokenError:
            error = "Invalid token."
            return Result.Fail(error)

        user_dict = dict(
            public_id=payload["sub"],
            admin=payload["admin"],
            token=access_token,
            expires_at=payload["exp"],
        )

        return Result.Ok(user_dict)
