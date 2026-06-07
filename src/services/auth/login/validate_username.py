from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.login import login_crud
from src.crud.auth.user import user_crud
from src.models.auth.login_session import Login
from src.schemas import LoginUsernameRequest, LoginUpdate


async def validate_username(
        self,
        db: AsyncSession,
        login_session: Login,
        obj_in: LoginUsernameRequest,
):

    # Check
    if login_session.login_method != 'username':
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

    # Check
    user = await user_crud.get_by_username(
        db=db,
        username=obj_in.username
    )
    if user is None:
        raise HTTPException(
            status_code=401,
            detail='User not found'
        )

    if user.is_locked:
        raise HTTPException(
            status_code=401,
            detail='User is locked'
        )

    await login_crud.update(
        db=db,
        id=login_session.id,
        obj_in=LoginUpdate(user_id=user.id)
    )
