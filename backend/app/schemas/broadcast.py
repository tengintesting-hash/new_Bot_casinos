from pydantic import BaseModel


class BroadcastCreate(BaseModel):
    type: str
    text: str = ""
    media_url: str = ""
    audience: str = "all"


class BroadcastOut(BroadcastCreate):
    id: int
    sent_ok: int
    sent_fail: int
    status: str

    class Config:
        from_attributes = True
