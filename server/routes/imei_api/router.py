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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36',
                'Origin': 'https://imeidata.info',
                'Referer': 'https://imeidata.info/',
                'Cookie': '_ga=GA1.1.1563153462.1741437805; _ga_9LSE50RRRS=GS1.1.1741441149.2.1.1741441234.0.0.0',
            }
            response = requests.post("https://imeidata.info/wp-content/plugins/imei-api/api.php",
                                headers=headers, 
                                data={
                "value": imei,
                "api_id": "c95b75fc-338b-49b8-9896-eb252fa464ab"
            })
            print(response)
            if response.status_code == 200:
                return {
                    "status": 200,
                    "message": "Successfully",
                    "data": response.json()['result']
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