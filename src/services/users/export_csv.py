
import csv
import io
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth.user import User


EXPORT_COLUMNS = (
    'id',
    'username',
    'first_name',
    'last_name',
    'email',
    'email_confirmed',
    'is_active',
    'is_locked',
    'created_at',
)


async def export_users_csv(db: AsyncSession) -> tuple[str, str]:
    ''' Export all users to CSV (without password). Returns (filename, csv_content). '''
    result = await db.execute(
        select(User).order_by(User.id.asc())
    )
    users = list(result.scalars().all())

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=EXPORT_COLUMNS)
    writer.writeheader()

    for user in users:
        writer.writerow({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'email_confirmed': user.email_confirmed,
            'is_active': user.is_active,
            'is_locked': user.is_locked,
            'created_at': user.created_at.isoformat() if user.created_at else '',
        })

    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    filename = f'users_export_{timestamp}.csv'
    return filename, buffer.getvalue()
