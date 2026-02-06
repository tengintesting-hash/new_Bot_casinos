from pydantic import BaseModel
from typing import Optional


class UserOut(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    referrer_id: Optional[int] = None
    balance_pro: int
    is_deposit: bool
    banned: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    balance_pro: Optional[int] = None
    is_deposit: Optional[bool] = None
    banned: Optional[bool] = None
