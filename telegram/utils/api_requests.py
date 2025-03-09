import requests

import jwt

from config.config import get_ALGORITHM, get_SECRET_KEY


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, get_SECRET_KEY(), algorithm=get_ALGORITHM())
    return encoded_jwt


def user_auth(user_tg_id):
    token = create_access_token({"tg_id": user_tg_id})
    req = requests.get(f"http://127.0.0.1:8000/user/auth/{token}")
    print(req)
    if req.status_code == 200:
        return req.json()
    return None


def whitelist_add_user(user_tg_id):
    token = create_access_token({"tg_id": user_tg_id})
    req = requests.get(f"http://127.0.0.1:8000/user/whitelist/add_in_whitelist/{token}")
    if req.status_code == 200:
        return req.json()
    return None


def whitelist_delete_user(user_tg_id):
    token = create_access_token({"tg_id": user_tg_id})
    req = requests.get(f"http://127.0.0.1:8000/user/whitelist/delete_from_whitelist/{token}")
    if req.status_code == 200:
        return req.json()
    return None


def get_imei_info(user_tg_id, imei):
    token = create_access_token({"tg_id": user_tg_id})
    req = requests.get(f"http://127.0.0.1:8000/imei/get_imei_info/{token}/{imei}")
    try:
        return req.json()
    except BaseException:
        return None


def get_imei_services_list():
    req = requests.get("http://127.0.0.1:8000/imei/get_imei_full_services")
    try:
        return req.json()
    except BaseException:
        return None