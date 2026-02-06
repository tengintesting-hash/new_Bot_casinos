from sqlalchemy import Column, Integer, String
from app.db.session import Base


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
