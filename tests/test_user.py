import time, json
from base64 import urlsafe_b64encode, urlsafe_b64decode

from flask_api_boilerplate.models.user import User


def test_encode_access_token(user):
    access_token = user.encode_access_token()
    assert isinstance(access_token, str)


def test_decode_access_token(user):
    access_token = user.encode_access_token()
    result = User.decode_access_token(access_token)

    assert result.success

    user_dict = result.value

    assert user.public_id == user_dict["public_id"]
    assert user.admin == user_dict["admin"]


def test_decode_access_token_expired(user):
    access_token = user.encode_access_token()

    time.sleep(6)

    result = User.decode_access_token(access_token)
    assert not result.success
    assert result.error == "Access token expired. Login again to renew."


def test_decode_acccess_token_invalid(user):
    access_token = user.encode_access_token()
    split = access_token.split(".")

    payload_base64 = split[1]
    pad_len = 4 - (len(payload_base64) % 4)

    payload_base64 += pad_len * "="
    payload_str = urlsafe_b64decode(payload_base64)
    payload = json.loads(payload_str)

    assert not payload["admin"]

    payload["admin"] = True
    payload_mod = json.dumps(payload)
    payload_mod_base64 = urlsafe_b64encode(payload_mod.encode())
    split[1] = payload_mod_base64.strip(b"=")
    access_token_mod = ".".join(str(split))
    assert not access_token == access_token_mod

    result = User.decode_access_token(access_token_mod)
    assert not result.success
    assert result.error == "Invalid token."
