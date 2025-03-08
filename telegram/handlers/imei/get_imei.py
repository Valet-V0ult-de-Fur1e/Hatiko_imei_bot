from forms.imei_form import Form
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.api_requests import user_auth, get_imei_info


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
            if check_imei['status'] == 200:
                await message.answer(check_imei['data'])
            elif check_imei['status'] == 404:
                await message.answer(check_imei['message'])
            elif check_imei['status'] == 500:
                await message.answer(check_imei['message'])
            elif check_imei['status'] == 400:
                await message.answer(check_imei['message'])
            elif check_imei['status'] == 404:
                await message.answer(check_imei['message'])
