
import csv
import io

from fastapi import HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.user import user_crud
from src.schemas import UserCreate
from src.schemas.users.csv import UserCsvImportRow, UserImportResponse
from src.utils.password import get_password_hash


REQUIRED_COLUMNS = {'username', 'first_name', 'last_name', 'email', 'password'}
OPTIONAL_COLUMNS = {'email_confirmed', 'is_active'}
ALLOWED_COLUMNS = REQUIRED_COLUMNS | OPTIONAL_COLUMNS


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None or value == '':
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'y'}


async def import_users_csv(
        db: AsyncSession,
        file: UploadFile,
) -> UserImportResponse:
    ''' Import users from CSV; skip rows that already exist by username or email. '''
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail='Upload a .csv file')

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail='CSV file is empty')

    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail='CSV must be UTF-8 encoded') from exc

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail='CSV header row is missing')

    headers = {name.strip().lower() for name in reader.fieldnames if name}
    missing = REQUIRED_COLUMNS - headers
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f'Missing required columns: {", ".join(sorted(missing))}',
        )

    unknown = headers - ALLOWED_COLUMNS
    if unknown:
        raise HTTPException(
            status_code=400,
            detail=f'Unknown columns: {", ".join(sorted(unknown))}',
        )

    created = 0
    skipped = 0
    errors: list[str] = []

    for row_number, row in enumerate(reader, start=2):
        if not any((value or '').strip() for value in row.values()):
            continue

        normalized = {
            key.strip().lower(): (value or '').strip()
            for key, value in row.items()
            if key
        }

        try:
            row_data = UserCsvImportRow(
                username=normalized['username'],
                first_name=normalized['first_name'],
                last_name=normalized['last_name'],
                email=normalized['email'],
                password=normalized['password'],
                email_confirmed=_parse_bool(normalized.get('email_confirmed')),
                is_active=_parse_bool(normalized.get('is_active'), default=True),
            )
        except ValidationError as exc:
            errors.append(f'Row {row_number}: {exc.errors()[0]["msg"]}')
            continue

        if await user_crud.get_by_username(db=db, username=row_data.username):
            skipped += 1
            continue

        if await user_crud.get_by_email(db=db, email=row_data.email):
            skipped += 1
            continue

        try:
            await user_crud.create(
                db=db,
                obj_in=UserCreate(
                    username=row_data.username,
                    first_name=row_data.first_name.title(),
                    last_name=row_data.last_name.title(),
                    email=row_data.email,
                    password=get_password_hash(row_data.password),
                    email_is_confirmed=row_data.email_confirmed,
                    is_active=row_data.is_active,
                ),
            )
            created += 1
        except HTTPException as exc:
            errors.append(f'Row {row_number}: {exc.detail}')
        except Exception as exc:
            errors.append(f'Row {row_number}: {exc}')

    return UserImportResponse(created=created, skipped=skipped, errors=errors)
