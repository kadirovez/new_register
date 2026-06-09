
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.deps.database import get_db
from src.deps.session import get_forgot_password_session
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas import Token
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.auth.forgot_password import ForgotPasswordLoginRequest, ForgotPasswordEmailRequest, \
    ForgotPasswordEmailOTPRequest, ForgotPasswordNewPasswordRequest, ForgotPasswordNewPasswordConfirmRequest
from src.schemas.base import StatusResponseSchema
from src.services.auth.forgot_password import forgot_password_service
from src.services.session import session_service
from src.utils.ip_address import get_ip

router = APIRouter(prefix='/forgot_password', tags=['forgot_password'])


@router.get('/start', response_model=Token)
async def start_session(
        request : Request,
        db : AsyncSession = Depends(get_db)
):
    '''
    Start your session, enter one of your credentials: email or username
    In case a username was entered, you will need to enter your full email to continue
    If succeeded, you will get an otp code to your mail
    After all, you will be able to change your password
    '''
    return await session_service.start_session(
        db=db,
        ip_address=get_ip(request),
        crud=forgot_password_crud,
        create_schema=CreateSessionSchema,
    )


@router.post('/identification')
async def validate_identifier(
        obj_in : ForgotPasswordLoginRequest,
        db: AsyncSession = Depends(get_db),
        forgot_password_session: ForgotPassword = Depends(get_forgot_password_session),
):
    return await forgot_password_service.validate_identifier(
        obj_in=obj_in,
        db=db,
        forgot_password_session=forgot_password_session,
    )


@router.post('/confirm-email')
async def confirm_email(
        obj_in: ForgotPasswordEmailRequest,
        db: AsyncSession = Depends(get_db),
        forgot_password_session: ForgotPassword = Depends(get_forgot_password_session),
) -> StatusResponseSchema:
    ''' Only for username identification step '''
    return await forgot_password_service.confirm_email(
        obj_in=obj_in,
        db=db,
        forgot_password_session=forgot_password_session,
    )


@router.get('send-email-otp')
async def send_email_otp(
        db: AsyncSession = Depends(get_db),
        forgot_password_session: ForgotPassword = Depends(get_forgot_password_session),
) -> StatusResponseSchema:
    ''' Send email OTP code '''
    return await forgot_password_service.forgot_password_send_email_otp(
        db=db,
        forgot_password_session=forgot_password_session,
    )


@router.post('validate_email_otp')
async def validate_email_otp(
        obj_in: ForgotPasswordEmailOTPRequest,
        db: AsyncSession = Depends(get_db),
        forgot_password_session : ForgotPassword = Depends(get_forgot_password_session)
) -> StatusResponseSchema:
    ''' Validate email OTP '''
    return await forgot_password_service.validate_email_otp(
        obj_in=obj_in,
        db=db,
        forgot_password_session=forgot_password_session,
    )


@router.post('/change-password')
async def change_password(
        obj_in: ForgotPasswordNewPasswordRequest,
        db: AsyncSession = Depends(get_db),
        forgot_password_session: ForgotPassword = Depends(get_forgot_password_session)
) -> StatusResponseSchema:
    ''' Validates new password '''
    return await forgot_password_service.change_password(
        obj_in=obj_in,
        db=db,
        forgot_password_session=forgot_password_session,
    )


@router.post('confirm-password')
async def confirm_password(
        obj_in: ForgotPasswordNewPasswordConfirmRequest,
        db: AsyncSession = Depends(get_db),
        forgot_password_session: ForgotPassword = Depends(get_forgot_password_session),
) -> StatusResponseSchema:
    ''' Confirms password and change '''
    return await forgot_password_service.confirm_password(
        obj_in=obj_in,
        db=db,
        forgot_password_session=forgot_password_session,
    )


@router.post('complete')
async def complete_forgot_password(
        db: AsyncSession = Depends(get_db),
        forgot_password_session: ForgotPassword = Depends(get_forgot_password_session)
):
    ''' Completes session and sets all changes in database '''
    return await forgot_password_service.complete_forgot_password(
        db=db,
        forgot_password_session=forgot_password_session,
    )


@router.delete('cancel-session')
async def cancel_forgot_password_session(
        db: AsyncSession = Depends(get_db),
        forgot_password_session: ForgotPassword = Depends(get_forgot_password_session)
):
    ''' Deletes forgot password session '''
    return await forgot_password_service.cancel_forgot_password(
        db=db,
        forgot_password_session=forgot_password_session,
    )

