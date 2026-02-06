import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest
from aiogram.utils.markdown import hbold
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Channel
from app.config import settings


async def ensure_user(session: AsyncSession, telegram_id: int, username: str | None, referrer_id: int | None) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user:
        return user
    user = User(telegram_id=telegram_id, username=username, referrer_id=referrer_id)
    session.add(user)
    if referrer_id:
        ref_result = await session.execute(select(User).where(User.telegram_id == referrer_id))
        referrer = ref_result.scalar_one_or_none()
        if referrer:
            referrer.balance_pro += 1000
    await session.commit()
    await session.refresh(user)
    return user


async def get_required_channels(session: AsyncSession) -> list[Channel]:
    result = await session.execute(select(Channel).where(Channel.is_required.is_(True)))
    channels = result.scalars().all()
    if channels:
        return channels
    return [
        Channel(channel_id=channel_id, link=f"https://t.me/{channel_id.lstrip('@')}", title=channel_id)
        for channel_id in settings.required_channels
    ]


async def has_all_subscriptions(bot: Bot, user_id: int, channels: list[Channel]) -> bool:
    for channel in channels:
        member = await bot.get_chat_member(chat_id=channel.channel_id, user_id=user_id)
        if member.status in {"left", "kicked"}:
            return False
    return True


def subscribe_keyboard(channels: list[Channel]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=channel.title, url=channel.link)]
        for channel in channels
    ]
    buttons.append([InlineKeyboardButton(text="Перевірити", callback_data="check_subs")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def register_handlers(dp: Dispatcher, session_factory) -> None:
    @dp.message(F.text.startswith("/start"))
    async def start_handler(message: Message):
        args = message.text.split(maxsplit=1)
        referrer_id = None
        if len(args) > 1 and args[1].startswith("ref_"):
            referrer_id = int(args[1].replace("ref_", ""))
        async with session_factory() as session:
            await ensure_user(session, message.from_user.id, message.from_user.username, referrer_id)
            channels = await get_required_channels(session)
        if channels and not await has_all_subscriptions(message.bot, message.from_user.id, channels):
            await message.answer(
                "Будь ласка, підпишіться на канали, щоб продовжити:",
                reply_markup=subscribe_keyboard(channels),
            )
            return
        await message.answer(
            f"{hbold('Вітаємо!')} Відкривайте казино через WebApp.",
        )

    @dp.callback_query(F.data == "check_subs")
    async def check_subs_handler(callback):
        async with session_factory() as session:
            channels = await get_required_channels(session)
        if await has_all_subscriptions(callback.bot, callback.from_user.id, channels):
            await callback.message.answer("Доступ відкрито! Відкривайте WebApp.")
            await callback.answer()
            return
        await callback.answer("Ще не всі підписки виконані.", show_alert=True)

    @dp.chat_join_request()
    async def join_request_handler(event: ChatJoinRequest):
        await event.approve()
