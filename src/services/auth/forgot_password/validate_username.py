
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.crud.auth.user import user_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.auth.forgot_password import ForgotPasswordUsernameRequest, ForgotPasswordUpdate, \
    ForgotPasswordMaskedEmailResponse
from src.utils.mask_email import mask_email


async def validate_username(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
        obj_in: ForgotPasswordUsernameRequest,
):
    # Check
    if forgot_password_session.login_method != 'username':
        raise HTTPException(
            status_code=401,
            detail='Wrong login method'
        )

    await forgot_password_crud.reset(
        db=db,
        db_obj=forgot_password_session,
        keep_fields={
            'login_method':True
        },
    )

    # Action
    user = await user_crud.get_by_username(
        db=db,
        username=obj_in.username,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail='User not found'
        )

    if user.is_locked:
        raise HTTPException(
            status_code=401,
            detail='User account is temporary locked, try again later'
        )

    await forgot_password_crud.update(
        db=db,
        id=forgot_password_session.id,
        obj_in=ForgotPasswordUpdate(
            user_id=user.id,
            username=user.username,
        )
    )

    return ForgotPasswordMaskedEmailResponse(masked_email=mask_email(user.email))

