from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    reward_pro = Column(Integer, default=0)
    link = Column(String(512), nullable=False)
    is_active = Column(Boolean, default=True)
