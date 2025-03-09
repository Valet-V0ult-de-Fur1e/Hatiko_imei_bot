from forms.imei_form import Form
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils.api_requests import user_auth, get_imei_info, get_imei_services_list


questionnaire_router = Router()


@questionnaire_router.message(F.text == "Проверить IMEI")
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('Введите IMEI (15 цифр без пробелов)')
    await state.set_state(Form.imei)

    
@questionnaire_router.message(F.text, Form.imei)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(imei=message.text)
    imei = message.text
    user_id = message.from_user.id
    req = user_auth(user_id)
    if req is None:
        await message.answer("Кажется какие-то проблемы на стороне сервера!!!")
    else:
        if req['in_whitelist']:
            check_imei = get_imei_info(user_id, imei)
            def get_device_info(data):
                head = data['header']
                body = data['items']
                out_message = f"""бренд: {head['brand']} \nмодель: {head['model']} \nimei: {head['imei']}"""
                for line in body:
                    if line['role'] == "header":
                        out_message += "\n" + line['title']
                    elif line['role'] == "item":
                        out_message += f"\n {line['title']}: {line['content']}"
                    elif line['role'] == "button":
                        break
                return out_message
            if check_imei['status'] == 200:
                await message.answer_photo(
                    photo=check_imei['data']['header']['photo'],
                    caption="Изображение устройства"
                    )
                await message.answer(get_device_info(check_imei['data']))
                for source in get_imei_services_list()['data'][:-1]:
                    source_services = f"{source['source']}"
                    for service in source['data']:
                        source_services += f"\n{service['name']} - {service['price']}"
                    await message.answer(source_services)
            elif check_imei['status'] == 404:
                await message.answer(check_imei['message'])
            elif check_imei['status'] == 500:
                await message.answer(check_imei['message'])
            elif check_imei['status'] == 400:
                await message.answer(check_imei['message'])
            elif check_imei['status'] == 404:
                await message.answer(check_imei['message'])
        else:
            await message.answer("Доступ запрещен")
