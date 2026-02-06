from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255))
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    balance_pro = Column(Integer, default=0)
    is_deposit = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    channel_id = Column(String(255), nullable=False)
    link = Column(String(512), nullable=False)
    title = Column(String(255), nullable=False)
    is_required = Column(Boolean, default=True)


class BroadcastLog(Base):
    __tablename__ = "broadcast_logs"

    id = Column(Integer, primary_key=True)
    type = Column(String(16), default="text")
    text = Column(String(2048), default="")
    media_url = Column(String(1024), default="")
    audience = Column(String(32), default="all")
    sent_ok = Column(Integer, default=0)
    sent_fail = Column(Integer, default=0)
    status = Column(String(32), default="pending")
