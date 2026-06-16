
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.database import get_db
from src.schemas.users.csv import UserImportResponse
from src.services.users import user_service

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/export-csv')
async def export_users_csv(
    db: AsyncSession = Depends(get_db),
):
    ''' Export all users from the main database as CSV (passwords are not included). '''
    filename, content = await user_service.export_users_csv(db=db)
    return StreamingResponse(
        iter([content]),
        media_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'},
    )


@router.post('/import-csv', response_model=UserImportResponse)
async def import_users_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    '''
    Import users from CSV.

    Required columns: username, first_name, last_name, email, password
    Optional columns: email_confirmed, is_active

    Existing users (same username or email) are skipped.
    '''
    return await user_service.import_users_csv(db=db, file=file)
