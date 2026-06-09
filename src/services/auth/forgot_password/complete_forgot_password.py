
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.crud.auth.user import user_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas import UserUpdate
from src.schemas.auth.forgot_password import ForgotPasswordUpdate
from src.schemas.base import StatusResponseSchema


async def complete_forgot_password(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
):
    # Check
    if not forgot_password_session.email_is_confirmed and forgot_password_session.new_password_is_confirmed:
        raise HTTPException(
            status_code=401,
            detail='Some of the conditions are not met'
        )

    # Action
    await forgot_password_crud.update(
        db=db,
        id=forgot_password_session.id,
        obj_in=ForgotPasswordUpdate(
            is_completed=True
        )
    )

    user = await user_crud.get(
        db=db,
        id=forgot_password_session.user_id
    )


    await user_crud.update(
        db=db,
        id=user.id,
        obj_in=UserUpdate(
            password=forgot_password_session.new_password
        )
    )

    return StatusResponseSchema(status=True)
