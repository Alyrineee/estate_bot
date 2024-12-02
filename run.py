import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.base.base import base
from app.admin.admin import admin
from app.agent.agent import agent
from app.manager.manager import manager
from app.middleware.authenticate import AuthenticateMiddleware
from config import TOKEN
from utils.google_api.models import ClientManager

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def manager_notify():
    while True:
        try:
            table = ClientManager()
            if table.get_unverifed_clients():
                for manager_id in table.get_managers():
                    await bot.send_message(
                        manager_id[0], "У Вас есть непроверенные заявки⚠️"
                    )
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")

        await asyncio.sleep(1800)


async def main():
    asyncio.create_task(manager_notify())
    dp.include_routers(base, agent, manager, admin)
    dp.message.middleware.register(AuthenticateMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit...")
