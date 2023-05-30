import hmac
import base64
import hashlib

from todoAPI.settings import SECRET_KEY


def create_hash(raw_string):
    hash_string = hmac.new(
        bytes(SECRET_KEY, 'utf-8'),
        msg=raw_string.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    hash_string = base64.b64encode(hash_string).decode()
    return hash_string
