

from typing import Optional, List, Dict, TypeVar
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.base import CRUDBase
from src.core.database import Base
from pydantic import BaseModel
from typing import TypeVar

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDSessionBase(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):

    async def get_by_session(self):
        pass

    async def get_by_ip(self):
        pass

    async def reset(self):
        pass

    async def cleanup(self):
        pass