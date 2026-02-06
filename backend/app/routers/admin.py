from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.routers.deps import get_admin_token
from app.models.offer import Offer
from app.models.channel import Channel
from app.models.user import User
from app.models.broadcast_log import BroadcastLog
from app.schemas.offer import OfferCreate, OfferOut
from app.schemas.channel import ChannelCreate, ChannelOut
from app.schemas.user import UserOut, UserUpdate
from app.schemas.broadcast import BroadcastCreate, BroadcastOut

router = APIRouter()


@router.get("/admin/offers", response_model=list[OfferOut], dependencies=[Depends(get_admin_token)])
async def get_offers(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Offer))
    return result.scalars().all()


@router.post("/admin/offers", response_model=OfferOut, dependencies=[Depends(get_admin_token)])
async def create_offer(payload: OfferCreate, session: AsyncSession = Depends(get_session)):
    offer = Offer(**payload.dict())
    session.add(offer)
    await session.commit()
    await session.refresh(offer)
    return offer


@router.post("/admin/offers/{offer_id}", response_model=OfferOut, dependencies=[Depends(get_admin_token)])
async def update_offer(offer_id: int, payload: OfferCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Offer).where(Offer.id == offer_id))
    offer = result.scalar_one()
    for key, value in payload.dict().items():
        setattr(offer, key, value)
    await session.commit()
    await session.refresh(offer)
    return offer


@router.get("/admin/channels", response_model=list[ChannelOut], dependencies=[Depends(get_admin_token)])
async def get_channels(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Channel))
    return result.scalars().all()


@router.post("/admin/channels", response_model=ChannelOut, dependencies=[Depends(get_admin_token)])
async def create_channel(payload: ChannelCreate, session: AsyncSession = Depends(get_session)):
    channel = Channel(**payload.dict())
    session.add(channel)
    await session.commit()
    await session.refresh(channel)
    return channel


@router.post("/admin/channels/{channel_id}", response_model=ChannelOut, dependencies=[Depends(get_admin_token)])
async def update_channel(channel_id: int, payload: ChannelCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one()
    for key, value in payload.dict().items():
        setattr(channel, key, value)
    await session.commit()
    await session.refresh(channel)
    return channel


@router.get("/admin/users", response_model=list[UserOut], dependencies=[Depends(get_admin_token)])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    return result.scalars().all()


@router.post("/admin/users/{user_id}", response_model=UserOut, dependencies=[Depends(get_admin_token)])
async def update_user(user_id: int, payload: UserUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()
    for key, value in payload.dict(exclude_none=True).items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/admin/broadcasts", response_model=BroadcastOut, dependencies=[Depends(get_admin_token)])
async def create_broadcast(payload: BroadcastCreate, session: AsyncSession = Depends(get_session)):
    log = BroadcastLog(**payload.dict())
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log
