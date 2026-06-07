
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.login import login_crud
from src.models.auth.login_session import Login
from src.schemas import LoginFinishResponse, LoginEmailOTPRequest, LoginUpdate


async def confirm_email_otp(
        self,
        db: AsyncSession,
        login_session: Login,
        obj_in: LoginEmailOTPRequest,
):

    # Check
    if not login_session.email_code_sent:
        raise HTTPException(
            status_code=401,
            detail='Email OTP code was not sent'
        )

    # Reset
    await login_crud.reset(
        db=db,
        db_obj=login_session,
        keep_fields={
            'login_method':True,
            'user_id':True,
            'username':True,
            'email':True,
            'email_matched':True,
            'email_code_sent':True,
            'email_code_id':True,
            'password_is_validated':True,
            'email_code_expire_at':True,
        }
    )

    if login_session.email_code_expire_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail='OTP code expired'
        )

    if login_session.email_code_sent != obj_in.email_otp:
        raise HTTPException(
            status_code=401,
            detail='Wrong otp code'
        )

    await login_crud.update(
        db=db,
        id=login_session.id,
        obj_in=LoginUpdate(
            email_is_confirmed=True,
            email_code_sent=None,
            email_code_id=None,
            email_code_expire_at=None,
        )
    )






