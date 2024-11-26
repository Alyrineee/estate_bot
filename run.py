import os
import asyncio

import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.base.base import base

load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()


async def main():
    dp.include_router(base)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit...")
