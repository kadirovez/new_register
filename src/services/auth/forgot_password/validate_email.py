
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.crud.auth.user import user_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.auth.forgot_password import ForgotPasswordEmailRequest, ForgotPasswordUpdate
from src.schemas.base import StatusResponseSchema


async def validate_email(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
        obj_in: ForgotPasswordEmailRequest,
):
    if forgot_password_session.login_method != 'email':
        raise HTTPException(
            status_code=401,
            detail='Login method is not email'
        )

    await forgot_password_crud.reset(
        db=db,
        db_obj=forgot_password_session,
        keep_fields={
            'login_method': True
        },
    )

    incoming_email = obj_in.email
    user = await user_crud.get_by_email(
        db=db,
        email=incoming_email,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail='User not found'
        )

    if user.is_locked:
        raise HTTPException(
            status_code=401,
            detail='User account is locked, try again later '
        )

    await forgot_password_crud.update(
        db=db,
        id=forgot_password_session.id,
        obj_in=ForgotPasswordUpdate(
            email_matched=True,
            user_id=user.id,
            email=incoming_email,
            username=user.username
        )
    )

    return StatusResponseSchema(status=True)

