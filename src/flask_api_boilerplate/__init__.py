""" flask_api Main Application Factory
    Create the Flask App and binds all the extensions to it
"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_api_boilerplate.config import get_config

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask("flask_api")
    app.config.from_object(get_config(config_name))

    """Register Blueprints"""
    from flask_api_boilerplate.api import api_blueprint

    app.register_blueprint(api_blueprint)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app
