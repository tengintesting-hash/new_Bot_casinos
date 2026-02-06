from pydantic import BaseModel


class ChannelCreate(BaseModel):
    channel_id: str
    link: str
    title: str
    is_required: bool = True


class ChannelOut(ChannelCreate):
    id: int

    class Config:
        from_attributes = True
