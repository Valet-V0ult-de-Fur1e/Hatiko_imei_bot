from aiogram.filters.state import State, StatesGroup


class Form(StatesGroup):
    imei = State()