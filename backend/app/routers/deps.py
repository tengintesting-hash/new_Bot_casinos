from fastapi import Header, HTTPException, status, Depends
from app.core.config import settings


def get_admin_token(x_admin_token: str = Header(default="")) -> str:
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Невірний токен")
    return x_admin_token


def get_user_id(x_user_id: str = Header(default="")) -> int:
    if not x_user_id.isdigit():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірна сесія")
    return int(x_user_id)
