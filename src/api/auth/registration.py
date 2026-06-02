from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.auth.registration import registration_crud
from src.deps.database import get_db
from src.deps.language import get_language
from src.deps.session import get_registration_session
from src.models.auth.registration import Registration
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.auth.registration import (
    RegistrationUsernameRequest,
    RegistrationConfirmPasswordRequest,
    RegistrationPasswordRequest,
    RegistrationPersonalInformationRequest,
    RegistrationGenerateTOTPResponse,
    RegistrationTOTPRequest,
    RegistrationPhoneRequest,
    RegistrationPhoneOTPRequest,
    RegistrationEmailRequest,
    RegistrationEmailOTPRequest,
    RegistrationSendOTPResponse,
)
from src.schemas.addons import Token
from src.services.auth.registration import registration_service
from src.services.session import session_service

router = APIRouter()


@router.get("/start", response_model=Token)
async def start_session(
        request: Request,
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Retrieve jwt token"""
    return await session_service.start_session(
        db=db,
        ip_address=request.client.host,
        crud=registration_crud,
        create_schema=CreateSessionSchema,
        rate_limit_minutes=settings.rate_limit_minutes,
        max_attempts=settings.max_attempts_per_ip
    )


@router.post("/username")
async def validate_username(
        obj_in: RegistrationUsernameRequest,
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Validate username"""
    return await registration_service.validate_username(
        obj_in=obj_in,
        registration_session=registration_session,
        db=db,
    )


@router.post("/password")
async def validate_password(
        obj_in: RegistrationPasswordRequest,
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Validate password"""
    return await registration_service.validate_password(
        obj_in=obj_in,
        registration_session=registration_session,
        db=db,
    )


@router.post("/confirm-password")
async def confirm_password(
        obj_in: RegistrationConfirmPasswordRequest,
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Confirm password"""
    return await registration_service.confirm_password(
        obj_in=obj_in,
        registration_session=registration_session,
        db=db,
    )


@router.post("/personal-information")
async def validate_personal_information(
        obj_in: RegistrationPersonalInformationRequest,
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Validate personal information"""
    return await registration_service.validate_personal_information(
        obj_in=obj_in,
        registration_session=registration_session,
        db=db,
    )


@router.get("/generate-totp", response_model=RegistrationGenerateTOTPResponse)
async def generate_totp(
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Generate totp code"""
    return await registration_service.generate_totp(
        registration_session=registration_session,
        db=db,
    )


@router.post("/confirm-totp")
async def confirm_totp(
        obj_in: RegistrationTOTPRequest,
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Confirm totp code"""
    return await registration_service.confirm_totp(
        obj_in=obj_in,
        registration_session=registration_session,
        db=db,
    )


@router.post("/phone")
async def validate_phone(
        obj_in: RegistrationPhoneRequest,
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Confirm phone number"""
    return await registration_service.validate_phone(
        obj_in=obj_in,
        registration_session=registration_session,
        db=db,
    )


@router.get("/send-phone-otp-code", response_model=RegistrationSendOTPResponse)
async def send_phone_otp_code(
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Send phone OTP code"""
    return await registration_service.send_phone_otp_code(
        registration_session=registration_session,
        db=db,
    )


@router.post("/phone-otp-code")
async def validate_phone_otp_code(
        obj_in: RegistrationPhoneOTPRequest,
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Validate phone OTP code"""
    return await registration_service.validate_phone_otp_code(
        obj_in=obj_in,
        registration_session=registration_session,
        db=db,
    )


@router.post("/email")
async def validate_email(
        obj_in: RegistrationEmailRequest,
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Validate email address"""
    return await registration_service.validate_email(
        obj_in=obj_in,
        registration_session=registration_session,
        db=db,
    )


@router.get("/send-email-otp-code", response_model=RegistrationSendOTPResponse)
async def send_email_otp_code(
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Send email OTP code"""
    return await registration_service.send_email_otp_code(
        registration_session=registration_session,
        db=db,
    )


@router.post("/email-otp-code")
async def validate_email_otp_code(
        obj_in: RegistrationEmailOTPRequest,
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Validate email OTP code"""
    return await registration_service.validate_email_otp_code(
        obj_in=obj_in,
        registration_session=registration_session,
        db=db,
    )


@router.get("/finish")
async def complete_registration(
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Complete registrations"""
    return await registration_service.complete_registration(
        registration_session=registration_session,
        db=db,
    )


@router.delete("/cancel")
async def cancel_registration(
        registration_session: Registration = Depends(get_registration_session),
        language: str = Depends(get_language),
        db: AsyncSession = Depends(get_db)
):
    """Cancel registration"""
    return await registration_service.cancel_registration(
        registration_session=registration_session,
        db=db,
    )
