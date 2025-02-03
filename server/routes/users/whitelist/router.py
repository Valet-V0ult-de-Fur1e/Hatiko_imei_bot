from fastapi import APIRouter

from db.models.user.interface import update_user
from utils.auth_utils import verify_access_token


router = APIRouter()


@router.get("/whitelist/add_in_whitelist/{token}")
async def add_user_in_whitelist(token: str) -> dict:
    user_info = verify_access_token(token=token)
    print(user_info)
    user_tg_id = user_info["tg_id"]
    check = await update_user(user_tg_id=user_tg_id, user_in_white_list_status=True)
    print(check)
    return check


@router.get("/whitelist/delete_from_whitelist/{token}")
async def delete_from_whitelist(token: str) -> dict:
    user_info = verify_access_token(token=token)
    user_tg_id = user_info["tg_id"]
    check = await update_user(user_tg_id=user_tg_id, user_in_white_list_status=False)
    return check