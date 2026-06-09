
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.crud.auth.user import user_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.auth.forgot_password import ForgotPasswordEmailRequest, ForgotPasswordUpdate
from src.schemas.base import StatusResponseSchema


async def confirm_email(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
        obj_in: ForgotPasswordEmailRequest,
):
    # Check
    if forgot_password_session.login_method != 'username':
        raise HTTPException(
            status_code=401,
            detail='Wrong login method'
        )

    if not forgot_password_session.user_id:
        raise HTTPException(
            status_code=401,
            detail='User not found'
        )

    # Action
    user = await user_crud.get(db=db, id=forgot_password_session.user_id)
    incoming_email = str(obj_in.email).lower()

    if incoming_email != user.email:
        raise HTTPException(
            status_code=401,
            detail='Entered email is not valid'
        )

    await forgot_password_crud.update(
        db=db,
        id=forgot_password_session.id,
        obj_in=ForgotPasswordUpdate(
            email_matched=True,
            email=incoming_email,
        )
    )

    return StatusResponseSchema(status=True)
