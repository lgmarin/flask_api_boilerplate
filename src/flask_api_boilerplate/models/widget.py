from flask_api_boilerplate import db
from flask_api_boilerplate.utils.datetime import utc_now


class Widget(db.Model):
    """Widget Model for the API"""

    __tablename__ = "widget"

    id = db.Column(db.Integer, primary_key=True, autoicrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    info_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=utc_now)
    dadline = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey("site_user.id"), nullable=False)
    owner = db.relationship("User", backref=db.backref("widgets"))

    def __repr__(self):
        return f"<Widget name={self.name}, info_url={self.info_url}"
