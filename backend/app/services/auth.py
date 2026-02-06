import hashlib
import hmac
from urllib.parse import parse_qsl
from fastapi import HTTPException, status
from app.core.config import settings


def validate_init_data(init_data: str) -> dict:
    if not init_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірні дані")

    parsed = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірні дані")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items(), key=lambda item: item[0])
    )
    secret_key = hashlib.sha256(settings.bot_token.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірні дані")

    return parsed


def verify_postback_signature(sub1: str, status_value: str, offer_id: str, signature: str) -> None:
    message = f"{sub1}:{status_value}:{offer_id}".encode()
    computed = hmac.new(settings.postback_secret.encode(), message, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed, signature):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Невірний підпис")
