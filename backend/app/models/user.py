from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.session import Base


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

    referrer = relationship("User", remote_side=[id])
