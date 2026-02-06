from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(64), nullable=False)
    amount_pro = Column(Integer, default=0)
    status = Column(String(32), default="pending")
