
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.base import StatusResponseSchema


async def cancel_forgot_password_session(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
):
    result = await forgot_password_crud.delete(
        db=db,
        id=forgot_password_session.id,
    )

    if not result:
        raise HTTPException(
            status_code=401,
            detail='Session invalid'
        )

    return StatusResponseSchema(status=True)
