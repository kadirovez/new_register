
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.login import login_crud
from src.crud.auth.user import user_crud
from src.models.auth.login_session import Login
from src.schemas import LoginEmailRequest, LoginUpdate


async def validate_email(
        self,
        db: AsyncSession,
        login_session: Login,
        obj_in: LoginEmailRequest,
):

    # Check
    if login_session.login_method != 'email':
        raise HTTPException(
            status_code=401,
            detail='...'
        )

    # Reset
    await login_crud.reset(
        db=db,
        db_obj=login_session,
        keep_fields={
            'login_method':True
        }
    )

    incoming_email = str(obj_in.email)

    user = await user_crud.get_by_email(
        db=db,
        email=incoming_email
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail='User not found'
        )

    if incoming_email != user.email:
        raise HTTPException(
            status_code=401,
            detail='Email address not found'
        )

    if user.is_locked:
        raise HTTPException(
            status_code=401,
            detail='User is locked'
        )

    await login_crud.update(
        db=db,
        db_in=login_session,
        obj_in=LoginUpdate(
            user_id=user.id,
            email_matched=True,
            email=incoming_email
        )
    )





