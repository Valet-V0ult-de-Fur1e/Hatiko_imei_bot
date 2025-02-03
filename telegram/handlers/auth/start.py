from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from utils.api_requests import user_auth

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    req = user_auth(user_id)
    if req is None:
        await message.answer("Кажется какие-то проблемы на стороне сервера!!!")
    else:
        if req['in_whitelist']:
            kb_list = [
                [KeyboardButton(text="Проверить IMEI"), KeyboardButton(text="Как получить IMEI?")]]
            keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
            await message.answer("Вы в белом списке! Хотите проверить информацию об устройстве? Или узнать как получить IMEI?", reply_markup=keyboard)
        else:
            kb_list = [
                [KeyboardButton(text="Запрос на вступление в белый список")]]
            keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Вас нет в белом списке! Отправьте запрос на добавление администратору!", reply_markup=keyboard)