import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from handlers.router import router

load_dotenv()
bot_token = getenv("TOKEN")

dp = Dispatcher(token=bot_token)

async def main():
    bot = Bot(token=bot_token)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Starting bot...")
    asyncio.run(main())