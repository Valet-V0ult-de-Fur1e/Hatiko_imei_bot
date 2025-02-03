from fastapi import APIRouter
from server.utils import get_user_info_from_token

router = APIRouter()

@router.get("/auth/{token}")
async def auth_user(token: str):
    check = await get_user_info_from_token(token)
    return check