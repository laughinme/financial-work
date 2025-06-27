import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start_handler(message: Message):
    await message.answer("Hello! I'm a placeholder bot.")

async def main():
    logging.basicConfig(level=logging.INFO)
    
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")
    
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    
    dp.message.register(start_handler, Command("start"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
