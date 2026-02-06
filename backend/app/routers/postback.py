from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.auth import verify_postback_signature
from app.models.user import User
from app.models.transaction import Transaction

router = APIRouter()


@router.post("/postback")
async def postback(
    sub1: str,
    status: str,
    offer_id: str,
    signature: str,
    session: AsyncSession = Depends(get_session),
):
    verify_postback_signature(sub1, status, offer_id, signature)
    result = await session.execute(select(User).where(User.telegram_id == int(sub1)))
    user = result.scalar_one_or_none()
    if not user:
        return {"status": "ignored"}

    if status == "deposit":
        user.is_deposit = True
        user.balance_pro += 10000
        transaction = Transaction(user_id=user.id, type="deposit_reward", amount_pro=10000, status="approved")
        session.add(transaction)
        if user.referrer_id:
            ref_result = await session.execute(select(User).where(User.id == user.referrer_id))
            referrer = ref_result.scalar_one_or_none()
            if referrer:
                referrer.balance_pro += 5000
                session.add(Transaction(user_id=referrer.id, type="ref_deposit_reward", amount_pro=5000, status="approved"))
    await session.commit()
    return {"status": "ok"}
