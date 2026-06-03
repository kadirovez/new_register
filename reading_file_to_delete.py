from typing import Optional, List, Dict, TypeVar
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.base import CRUDBase
from src.core.database import Base
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDSessionBase(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD for session-based models."""
    pass

    async def get_by_session(
            self,
            db: AsyncSession,
            session: str
    ) -> Optional[ModelType]:
        """Get record by session token."""
        result = await db.execute(
            select(self.model).where(self.model.session == session)
        )
        return result.scalar_one_or_none()

    async def get_by_ip(
            self,
            db: AsyncSession,
            ip_address: str,
            skip: int = 0,
            limit: int = 100
    ) -> List[ModelType]:
        """Get records by IP address."""
        result = await db.execute(
            select(self.model)
            .where(self.model.ip_address == ip_address)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_recent_by_ip(
            self,
            db: AsyncSession,
            ip_address: str,
            minutes: int
    ) -> int:
        """Count recent sessions from specific IP within time window."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=minutes)

        result = await db.execute(
            select(func.count(self.model.id))
            .where(
                self.model.ip_address == ip_address,
                self.model.created_at >= cutoff_time
            )
        )
        return result.scalar_one()

    async def reset(
            self,
            db: AsyncSession,
            db_obj: ModelType,
            keep_fields: Dict[str, bool] | None = None
    ) -> ModelType:
        """
        Reset session fields while keeping specified fields.
        """
        if keep_fields is None:
            keep_fields = {}

        # Build reset data
        reset_data = {}
        for field, reset_value in self.reset_values.items():
            if not keep_fields.get(field, False):
                reset_data[field] = reset_value

        # Update session
        for field, value in reset_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def cleanup(
            self,
            db: AsyncSession,
            expire_minutes: int | None = None
    ) -> int:
        """
        Delete incomplete sessions older than configured time.
        """
        if expire_minutes is None:
            expire_minutes = settings.session_expire_minutes

        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=expire_minutes)

        # Delete expired incomplete sessions
        result = await db.execute(
            delete(self.model).where(
                self.model.created_at < cutoff_time,
                # self.model.is_completed == False
            )
        )
        await db.commit()

        return result.rowcount


