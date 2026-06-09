
from datetime import timezone, datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.auth.forgot_password import ForgotPasswordEmailOTPRequest, ForgotPasswordUpdate
from src.schemas.base import StatusResponseSchema


async def validate_email_otp(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
        obj_in: ForgotPasswordEmailOTPRequest,
):
    # Check
    if not forgot_password_session.email_code_sent:
        raise HTTPException(
            status_code=401,
            detail='Email OTP code was not sent'
        )

    await forgot_password_crud.reset(
        db=db,
        db_obj=forgot_password_session,
        keep_fields={
            'login_method':True,
            'user_id':True,
            'email':True,
            'username':True,
            'email_is_confirmed':True,
            'email_matched':True,
            'email_code_sent':True,
            'email_code_expire_at':True,
            'email_code_id':True
        }
    )

    expire_at = forgot_password_session.email_code_expire_at
    if expire_at and expire_at.tzinfo is None:
        expire_at = expire_at.replace(tzinfo=timezone.utc)
    if expire_at and expire_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail='OTP code expired'
        )

    if forgot_password_session.email_code_sent != obj_in.email_otp:
        raise HTTPException(
            status_code=401,
            detail='OTP code is not valid'
        )

    # Action
    await forgot_password_crud.update(
        db=db,
        id=forgot_password_session.id,
        obj_in=ForgotPasswordUpdate(
            email_is_confirmed=True,
            email_code_sent=None,
            email_code_expire_at=None,
            email_code_id=None,
        )
    )

    return StatusResponseSchema(status=True)

