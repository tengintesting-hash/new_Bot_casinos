from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    channel_id = Column(String(255), nullable=False)
    link = Column(String(512), nullable=False)
    title = Column(String(255), nullable=False)
    is_required = Column(Boolean, default=True)
