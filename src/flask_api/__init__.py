from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from flask_api.config import get_config

cors = CORS()


def create_app(config_name):
    app = Flask("flask_api")
    app.config.from_object(get_config(config_name))

    return app
