from fastapi import APIRouter
from config.config import get_API_TOKEN
from server.utils import get_user_info_from_token, validate_imei
import requests
from bs4 import BeautifulSoup

router = APIRouter(prefix='/imei', tags=['IMEI'])


@router.get('/get_imei_full_services')
async def get_imei_full_services():
    filtered_dash_imei_info = []
    try:
        req_dash_imei_info = requests.get("https://dash.imei.info/api/service/services/?API_KEY=9ef71e10-a957-4fc1-ad51-be0e006f680d")
        filtered_dash_imei_info = list(filter(
            lambda x: 'imei' in x['required_fields'],
            req_dash_imei_info.json()
        ))
    except Exception:
        print("dash_imei_info fail")
    try:
        headers = {
            'authorization': "Bearer 72512|h52JLMpN0bdXFW3zqH3Q69YJ1ydOoWsgXEGQqloK",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36',
            'Origin': 'https://imeidata.info',
            'Referer': 'https://imeidata.info/',
            'Cookie': '_ga=GA1.1.1563153462.1741437805; _ga_9LSE50RRRS=GS1.1.1741441149.2.1.1741441234.0.0.0',
        }
        req_alpha_imeicheck_com = requests.get("https://alpha.imeicheck.com/api/services", headers=headers)
        filtered_alpha_imeicheck_com = list(filter(
            lambda x: 'imei' in x['name'].lower(),
            req_alpha_imeicheck_com.json()
        ))
    except Exception:
        print("alpha_imeicheck_com fail")
    try:
        html = requests.get("https://iunlocker.com/price/").text  # Вставьте ваш HTML сюда
        soup = BeautifulSoup(html, 'html.parser')
        services = []
        for service in soup.select('li .service-line'):
            third_col = service.select_one('.service-line__third-col')
            worktime = third_col.select_one('.service-line__worktime').get_text(strip=True)
            price_elem = third_col.select_one('.service-line__price')
            price = ''.join(filter(lambda x: x.isdigit() or x == '.', price_elem.get_text()))
            details_link = third_col.select_one('a[href]')['href']
            service_data = {
                'worktime': worktime,
                'price': float(price),
                'details_url': details_link
            }
            first_col = service.select_one('.service-line__first-col')
            service_data['name'] = first_col.select_one('.service-line__title').get_text(strip=True)
            service_data['image'] = first_col.select_one('img')['src']
            services.append(service_data)
    except Exception:
        print("iunlocker_com fail")
    return {
        "data": [
            {
                "source": "dash.imei.info",
                "data": filtered_dash_imei_info
            },
            {
                "source": "alpha.imeicheck.com",
                "data": filtered_alpha_imeicheck_com
            },
            {
                "source": "iunlocker.com",
                "data": services
            }
        ]
    }

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