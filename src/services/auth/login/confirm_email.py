
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.login import login_crud
from src.crud.auth.user import user_crud
from src.models.auth.login_session import Login
from src.schemas import LoginConfirmEmailRequest, LoginUpdate
from src.schemas.base import StatusResponseSchema


async def confirm_email(
        self,
        db: AsyncSession,
        login_session: Login,
        obj_in: LoginConfirmEmailRequest,
) -> StatusResponseSchema:
    ''' Email confirmation step. Use only if login method is username '''

    # Reset
    await login_crud.reset(
        db=db,
        db_obj=login_session,
        keep_fields={
            'login_method' : True,
            'user_id' : True,
            'username' : True,
            'password_is_validated' : True
        }
    )

    # Check
    user = await user_crud.get(db=db, id=login_session.user_id)
    if login_session.login_method != 'email':
        raise HTTPException(
            status_code=401,
            detail='Wrong login method'
        )

    if login_session.password_is_validated:
        raise HTTPException(
            status_code=401,
            detail='Validate password first'
        )

    if not user.email_confirmed:
        raise HTTPException(
            status_code=401,
            detail='Confirm your email first'
        )

    incoming_email = str(obj_in.email)

    if incoming_email != user.email:
        raise HTTPException(
            status_code=401,
            detail='Wrong email address'
        )

    await login_crud.update(
        db=db,
        id=login_session.id,
        obj_in=LoginUpdate(
            email_matched=True
        )
    )













