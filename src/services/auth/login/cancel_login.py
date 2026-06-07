
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.login import login_crud
from src.models.auth.login_session import Login


async def cancel_login(
        self,
        db: AsyncSession,
        login_session: Login,
):
    result = await login_crud.delete(
        db=db,
        id=login_session.id
    )
    if not result:
        raise HTTPException(
            status_code=401,
            detail='Session invalid'
        )