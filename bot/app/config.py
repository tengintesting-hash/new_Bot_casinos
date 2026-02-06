import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:////data/app.db")
    webapp_url: str = os.getenv("WEBAPP_URL", "")
    bot_username: str = os.getenv("BOT_USERNAME", "")
    required_channels: list[str] = field(
        default_factory=lambda: [
            c.strip() for c in os.getenv("REQUIRED_CHANNELS", "").split(",") if c.strip()
        ]
    )


settings = Settings()
