from datetime import timedelta, datetime, timezone

from fastapi import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.auth.login import login_crud
from src.crud.auth.main import main_crud
from src.crud.auth.user import user_crud
from src.models.auth.login_session import Login
from src.schemas import LoginUpdate, UserUpdate, Token
from src.schemas.auth.main import MainCreate
from src.utils.generator import generate_string
from src.utils.jwt_token import create_access_token


async def complete_login(
        self,
        request: Request,
        login_session: Login,
        db: AsyncSession,
):
    # Check
    if login_session.is_completed:
        raise HTTPException(
            status_code=401,
            detail='Session already completed'
        )

    if login_session.email_is_confirmed and login_session.password_is_validated:
        await login_crud.update(
            db=db,
            id=login_session.id,
            obj_in=LoginUpdate(
                is_completed=True
            )
        )
    else:
        raise HTTPException(
            status_code=401,
            detail='...'
        )

    if login_session.is_completed:
        ip_address = request.client.host
        session = generate_string(256, digits=True, lowercase=True, uppercase=True)
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        await main_crud.create(
            db=db,
            obj_in=MainCreate(
                user_id=login_session.user_id,
                ip_address=login_session.ip_address,
                session=session
            ),
        )

        access_token = create_access_token(
            data={
                'session':session,
                'ip_address':ip_address,
            },
            expires_delta=access_token_expires
        )

        return Token.model_validate({
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": str(datetime.now(timezone.utc) + access_token_expires),
        })

    raise HTTPException(
        status_code=401,
        detail='Something went wrong'
    )






















