import json
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode

from flask_api_boilerplate.models.user import User


def test_decode_access_token(user):
    access_token = user.encode_access_token()
    result = User.decode_access_token(access_token)

    assert result.success

    user_dict = result.value

    assert user.public_id == user_dict["public_id"]
    assert user.admin == user_dict["admin"]
