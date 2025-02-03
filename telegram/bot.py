import asyncio

from aiogram import Bot, Dispatcher
from handlers import router_auth, router_whitelist, router_imei, router_imei_form
from aiogram.fsm.storage.memory import MemoryStorage

bot = None

async def main():
    bot = Bot(token="7941033553:AAEYj6UqsCEifMtpRSLpPULkbhSrjvUhdWY")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router_auth)
    dp.include_router(router_whitelist)
    dp.include_router(router_imei)
    dp.include_router(router_imei_form)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())