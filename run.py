import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.base.base import base
from dotenv import load_dotenv
from estate_bot.app.agent.agent import agent
from estate_bot.config import TOKEN

load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(base, agent)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit...")
