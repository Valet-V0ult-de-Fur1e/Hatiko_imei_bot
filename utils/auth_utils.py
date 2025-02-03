import jwt

from config.config import get_SECRET_KEY, get_ALGORITHM


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, get_SECRET_KEY(), algorithm=get_ALGORITHM())
    return encoded_jwt


def verify_access_token(token):
    print(token)
    try:
        payload = jwt.decode(token, get_SECRET_KEY(), algorithms=[get_ALGORITHM()])
        return payload
    except jwt.PyJWTError:
        return None
