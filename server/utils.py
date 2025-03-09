from db.models.user.interface import find_user_by_id_or_create_new
from utils.auth_utils import verify_access_token


async def get_user_info_from_token(token:str):
    user_info = verify_access_token(token=token)
    user_tg_id = user_info["tg_id"]
    check = await find_user_by_id_or_create_new(user_tg_id=user_tg_id)
    return check

def validate_imei(imei: str) -> bool:
    if len(imei) != 15 or not imei.isdigit():
        return False
    total = 0
    for i in range(15):
        digit = int(imei[i])
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0