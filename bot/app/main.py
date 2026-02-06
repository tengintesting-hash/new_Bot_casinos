import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from app.config import settings
from app.db import engine, Base, AsyncSessionLocal
from app.handlers import register_handlers
from app.broadcast import run_broadcast_worker


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    register_handlers(dp, AsyncSessionLocal)

    asyncio.create_task(run_broadcast_worker(bot, AsyncSessionLocal))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
