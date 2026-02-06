from pydantic import BaseModel


class OfferCreate(BaseModel):
    title: str
    reward_pro: int
    link: str
    is_active: bool = True


class OfferOut(OfferCreate):
    id: int

    class Config:
        from_attributes = True
