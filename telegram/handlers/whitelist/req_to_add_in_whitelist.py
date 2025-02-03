import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from utils.api_requests import whitelist_add_user

router = Router()


@router.message(F.text == "Запрос на вступление в белый список")
async def cmd_start(message: Message):
    user_id = message.from_user.id
    req = whitelist_add_user(user_id)
    print(req)
    await asyncio.sleep(5)
    if req is None:
        await message.answer("Кажется какие-то проблемы на стороне сервера!!!")
    else:
        kb_list = [
            [KeyboardButton(text="Проверить IMEI"), KeyboardButton(text="Как получить IMEI?")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Администрация приняла вашу заявку! Хотите проверить информацию об устройстве? Или узнать как получить IMEI?", reply_markup=keyboard)