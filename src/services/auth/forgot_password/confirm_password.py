
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.auth.forgot_password import ForgotPasswordNewPasswordConfirmRequest, ForgotPasswordUpdate
from src.schemas.base import StatusResponseSchema
from src.utils.password import verify_password


async def confirm_password(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
        obj_in: ForgotPasswordNewPasswordConfirmRequest,
):

    # Check
    if not forgot_password_session.new_password:
        raise HTTPException(
            status_code=401,
            detail='Enter your password first'
        )

    # Reset
    await forgot_password_crud.reset(
        db=db,
        db_obj=forgot_password_session,
        keep_fields={
            'login_method':True,
            'user_id':True,
            'username':True,
            'email':True,
            'email_is_confirmed':True,
            'email_is_matched':True,
            'new_password':True,
            'new_password_is_validated':True,
        }
    )

    # Action
    if not verify_password(obj_in.password_confirm, forgot_password_session.new_password):
        raise HTTPException(
            status_code=401,
            detail='Entered password did not match'
        )

    await forgot_password_crud.update(
        db=db,
        id=forgot_password_session.id,
        obj_in=ForgotPasswordUpdate(
            new_password_is_confirmed=True
        )
    )

    return StatusResponseSchema(status=True)

