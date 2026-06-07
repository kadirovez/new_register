
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.register import registration_crud
from src.models.auth.register_session import Registration
from src.schemas.auth.registration import RegistrationEmailOTPRequest, RegistrationUpdate
from src.schemas.base import StatusResponseSchema


async def confirm_email_otp(
        db: AsyncSession,
        registration_session: Registration,
        obj_in: RegistrationEmailOTPRequest,
) -> StatusResponseSchema:
    ''' Checks email otp code '''


    if not registration_session.email_code_sent:
        raise HTTPException(
            status_code=400,
            detail='Request otp first'
        )

    await registration_crud.reset(
        db=db,
        db_obj=registration_session,
        keep_fields={
            'username':True,
            'first_name':True,
            'last_name':True,
            'email':True,
            'email_code_sent':True,
            'email_code_id':True,
            'email_code_expire_at':True,
        }
    )

    if registration_session.email_code_expire_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail='OTP expired'
        )

    # Check otp code
    if registration_session.email_code_sent != obj_in.email_otp:
        raise HTTPException(
            status_code=401,
            detail='Invalid otp code'
        )

    await registration_crud.update(
        db=db,
        id=registration_session.id,
        obj_in=RegistrationUpdate(
            email_is_confirmed=True
        ),
    )

    return StatusResponseSchema(status=True)
