import json
from fastapi import APIRouter, Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.auth import validate_init_data
from app.models.offer import Offer
from app.models.user import User
from app.schemas.offer import OfferOut
from app.schemas.user import UserOut
from app.routers.deps import get_user_id

router = APIRouter()


@router.post("/api/auth", response_model=UserOut)
async def auth_user(
    init_data: str = Header(default="", alias="initData"),
    session: AsyncSession = Depends(get_session),
):
    data = validate_init_data(init_data)
    user_payload = json.loads(data.get("user", "{}"))
    telegram_id = int(user_payload.get("id"))
    username = user_payload.get("username")
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


@router.get("/api/me", response_model=UserOut)
async def get_me(
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()
    return user


@router.get("/api/offers", response_model=list[OfferOut])
async def list_offers(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Offer).where(Offer.is_active.is_(True)))
    return result.scalars().all()
