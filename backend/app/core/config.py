from pydantic import BaseModel
import os


class Settings(BaseModel):
    bot_token: str = os.getenv("BOT_TOKEN", "")
    admin_token: str = os.getenv("ADMIN_TOKEN", "")
    postback_secret: str = os.getenv("POSTBACK_SECRET", "")
    webapp_url: str = os.getenv("WEBAPP_URL", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:////data/app.db")
    bot_username: str = os.getenv("BOT_USERNAME", "")
    required_channels: list[str] = [
        c.strip() for c in os.getenv("REQUIRED_CHANNELS", "").split(",") if c.strip()
    ]


settings = Settings()
