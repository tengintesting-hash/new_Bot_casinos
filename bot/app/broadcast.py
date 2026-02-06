import asyncio
from aiogram import Bot
from sqlalchemy import select
from app.models import BroadcastLog, User


async def run_broadcast_worker(bot: Bot, session_factory) -> None:
    while True:
        async with session_factory() as session:
            result = await session.execute(select(BroadcastLog).where(BroadcastLog.status == "pending"))
            logs = result.scalars().all()
            for log in logs:
                log.status = "processing"
                await session.commit()
                if log.audience == "deposit_only":
                    user_result = await session.execute(select(User).where(User.is_deposit.is_(True)))
                else:
                    user_result = await session.execute(select(User))
                users = user_result.scalars().all()
                for user in users:
                    try:
                        if log.type == "photo" and log.media_url:
                            await bot.send_photo(user.telegram_id, log.media_url, caption=log.text)
                        elif log.type == "video" and log.media_url:
                            await bot.send_video(user.telegram_id, log.media_url, caption=log.text)
                        else:
                            await bot.send_message(user.telegram_id, log.text)
                        log.sent_ok += 1
                    except Exception:
                        log.sent_fail += 1
                    await asyncio.sleep(0.05)
                log.status = "done"
                await session.commit()
        await asyncio.sleep(2)
