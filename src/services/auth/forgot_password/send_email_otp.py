
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.auth.forgot_password import forgot_password_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.auth.forgot_password import ForgotPasswordUpdate
from src.schemas.base import StatusResponseSchema
from src.utils.email import send_email
from src.utils.generator import generate_otp


async def forgot_password_send_email_otp(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
) -> StatusResponseSchema:

    # Check
    if not forgot_password_session.email:
        raise HTTPException(
            status_code=401,
            detail='Enter your email first'
        )

    if not forgot_password_session.email_matched:
        raise HTTPException(
            status_code=401,
            detail='Email is not validated'
        )

    # Create otp code
    otp_code, otp_code_id, otp_expire_at = generate_otp(
        length=6,
        timeout=settings.email_code_timeout,
    )
    otp_code = otp_code[:6].zfill(6)

    # Action
    await send_email(otp_code)

    await forgot_password_crud.update(
        db=db,
        id=forgot_password_session.id,
        obj_in=ForgotPasswordUpdate(
            email_code_sent=otp_code,
            email_code_id=otp_code_id,
            email_code_expire_at=otp_expire_at
        )
    )

    return StatusResponseSchema(status=True)

