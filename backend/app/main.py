from fastapi import FastAPI
from app.db.session import engine, Base
from app.routers import public, admin, postback

app = FastAPI(title="Telegram Casino API")


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(public.router)
app.include_router(admin.router)
app.include_router(postback.router)
