
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.auth.login import login_crud
from src.crud.auth.user import user_crud
from src.models.auth.login_session import Login
from src.schemas import LoginUpdate
from src.schemas.base import StatusResponseSchema
from src.utils.email import send_email
from src.utils.generator import generate_otp


async def send_email_otp(
        self,
        db: AsyncSession,
        login_session: Login,
):

    user = await user_crud.get(db=db, id=login_session.user_id)

    # Check
    if not login_session.email:
        raise HTTPException(
            status_code=401,
            detail='Enter email first'
        )

    if not user.email_confirmed:
        raise HTTPException(
            status_code=401,
            detail='Confirm email first'
        )

    # Reset
    await login_crud.reset(
        db=db,
        db_obj=login_session,
        keep_fields={
            'user_id':True,
            'login_method':True,
            'username':True,
            'email':True,
            'password_is_validated':True,
        }
    )

    otp_code, otp_code_id, otp_expire_at = generate_otp(length=4, timeout=settings.email_code_timeout)

    await send_email(otp_code)

    await login_crud.update(
        db=db,
        id=login_session.id,
        obj_in=LoginUpdate(
            email_code_sent=otp_code,
            email_code_id=otp_code_id,
            email_code_expire_at=otp_expire_at,
        )
    )












