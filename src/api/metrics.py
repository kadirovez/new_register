
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.database import get_db
from src.services.users.metrics import get_all_data

router = APIRouter(prefix='/metrics', tags=['metrics'])

@router.get('/')
async def metrics(
        db: AsyncSession = Depends(get_db)
):
    return await get_all_data(db=db)
