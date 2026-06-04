
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth.user import User


class CRUDUser:
    ''' CRUD for user records '''

    model = User

    async def get_by_username(
            self,
            db: AsyncSession,
            username: str,
    ) -> Optional[User]:
        ''' Get user by username '''
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()


    async def get_by_email(
            self,
            db: AsyncSession,
            email: str
    ) -> Optional[User]:
        ''' Gets user by email '''
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def disable(
            self,
            db: AsyncSession,
            db_obj: User,
    ) -> User:
        ''' Enables account '''
        db_obj.is_active = False
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


    async def enable(
            self,
            db: AsyncSession,
            db_obj: User,
    ) -> User:
        ''' Disables account '''
        db_obj.is_active = True
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj



user_crud = CRUDUser()
