
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.auth.forgot_password import ForgotPasswordNewPasswordRequest, ForgotPasswordUpdate
from src.schemas.base import StatusResponseSchema
from src.utils.password import get_password_hash


async def change_password(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
        obj_in: ForgotPasswordNewPasswordRequest
):
    # Check
    if not forgot_password_session.email_is_confirmed:
        raise HTTPException(
            status_code=401,
            detail='Confirm your email first'
        )

    await forgot_password_crud.reset(
        db=db,
        db_obj=forgot_password_session,
        keep_fields={
            'login_method':True,
            'username':True,
            'user_id':True,
            'email':True,
            'email_is_confirmed':True,
            'email_matched':True,
        }
    )

    # Action
    await forgot_password_crud.update(
        db=db,
        id=forgot_password_session.id,
        obj_in=ForgotPasswordUpdate(
            new_password=get_password_hash(obj_in.new_password),
            new_password_is_validated=True,
        )
    )

    return StatusResponseSchema(status=True)
