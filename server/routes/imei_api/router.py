from fastapi import APIRouter
from config.config import get_API_TOKEN
from server.utils import get_user_info_from_token, validate_imei
import requests


router = APIRouter(prefix='/imei', tags=['IMEI'])


@router.get('/get_imei_info/{token}/{imei}')
async def get_imei_info(token: str, imei: str):
    check = await get_user_info_from_token(token)
    if check["in_whitelist"]:
        if validate_imei(imei):
            response = requests.post('https://imeicheck.net/api/check-imei', data={
            'imei': imei,
            'token': get_API_TOKEN()
            })
            print(response)
            if response.status_code == 201:
                return {
                    "status": 200,
                    "message": "Successfully",
                    "data": response.json().get("properties", {})
                }
            if response.status_code == 404:
                return {
                    "status": 404,
                    "message": "Устройство не обнаружено"
                }
            if response.status_code >= 500:
                return {
                    "status": 500,
                    "message": "Сервис не работает! Повторите запрос попозже!"
                }
        return {
            "status": 400,
            "message": "Неккоректный IMEI"
        }
    return {
        "status": 403,
        "message": "Пользователь не находится в белом списке"
    }