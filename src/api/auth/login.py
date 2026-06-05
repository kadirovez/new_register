from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.auth.login import login_crud
from src.deps.database import get_db
from src.deps.session import get_login_session
from src.models.auth.login_session import Login
from src.schemas.addons import Token
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.auth.login import (
    LoginUsernameRequest,
    LoginEmailRequest,
    LoginConfirmEmailRequest,
    LoginPasswordRequest,
    LoginEmailOTPRequest,
    LoginMaskedEmailResponse,
    LoginFinishResponse,
)
from src.schemas.base import StatusResponseSchema
from src.services.auth.login import login_service
from src.services.session import session_service

router = APIRouter(prefix="/login", tags=["login"])


@router.get("/start", response_model=Token)
async def start_login(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    return await session_service.start_session(
        db=db,
        request=request,
        crud=login_crud,
        create_schema=CreateSessionSchema,
        rate_limit_minutes=settings.rate_limit_minutes,
        max_attempts=settings.max_attempts_per_ip,
    )


@router.post("/username", response_model=LoginMaskedEmailResponse)
async def login_by_username(
    obj_in: LoginUsernameRequest,
    login_session: Login = Depends(get_login_session),
    db: AsyncSession = Depends(get_db),
):
    return await login_service.start_by_username(
        db=db,
        login_session=login_session,
        obj_in=obj_in,
    )


@router.post("/email", response_model=StatusResponseSchema)
async def login_by_email(
    obj_in: LoginEmailRequest,
    login_session: Login = Depends(get_login_session),
    db: AsyncSession = Depends(get_db),
):
    return await login_service.start_by_email(
        db=db,
        login_session=login_session,
        obj_in=obj_in,
    )


@router.post("/confirm-email", response_model=StatusResponseSchema)
async def confirm_email(
    obj_in: LoginConfirmEmailRequest,
    login_session: Login = Depends(get_login_session),
    db: AsyncSession = Depends(get_db),
):
    return await login_service.confirm_email(
        db=db,
        login_session=login_session,
        obj_in=obj_in,
    )


@router.post("/password", response_model=StatusResponseSchema)
async def submit_password(
    obj_in: LoginPasswordRequest,
    login_session: Login = Depends(get_login_session),
    db: AsyncSession = Depends(get_db),
):
    return await login_service.submit_password(
        db=db,
        login_session=login_session,
        obj_in=obj_in,
    )


@router.get("/send-email-otp", response_model=StatusResponseSchema)
async def send_email_otp(
    login_session: Login = Depends(get_login_session),
    db: AsyncSession = Depends(get_db),
):
    return await login_service.send_email_otp(
        db=db,
        login_session=login_session,
    )


@router.post("/email-otp", response_model=LoginFinishResponse)
async def confirm_email_otp(
    obj_in: LoginEmailOTPRequest,
    login_session: Login = Depends(get_login_session),
    db: AsyncSession = Depends(get_db),
):
    return await login_service.confirm_email_otp(
        db=db,
        login_session=login_session,
        obj_in=obj_in,
    )


@router.delete("/cancel", response_model=StatusResponseSchema)
async def cancel_login(
    login_session: Login = Depends(get_login_session),
    db: AsyncSession = Depends(get_db),
):
    return await login_service.cancel(
        db=db,
        login_session=login_session,
    )
