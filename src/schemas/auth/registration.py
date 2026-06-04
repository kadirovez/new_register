
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.schemas.base import BaseResponseSchema
from src.schemas.fields import (
    USERNAME_FIELD,
    NAME_FIELD,
    PASSWORD_FIELD,
    EMAIL_FIELD,
)


class RegistrationProfileRequest(BaseModel):
    """Step 1: first name, last name, username, email."""

    first_name: NAME_FIELD
    last_name: NAME_FIELD
    username: USERNAME_FIELD
    email: EMAIL_FIELD


class RegistrationPasswordRequest(BaseModel):
    """Step 2: set password."""

    password: PASSWORD_FIELD


class RegistrationConfirmPasswordRequest(BaseModel):
    """Step 3: confirm password."""

    confirm_password: PASSWORD_FIELD


class RegistrationUpdate(BaseModel):
    """Fields allowed when updating a registration session."""

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_is_confirmed: Optional[bool] = None
    is_completed: Optional[bool] = None


class RegistrationFinishResponse(BaseResponseSchema):
    """Response after successful registration."""

    user_id: int


# --- Not used in current registration flow ---
# class RegistrationEmailOTPRequest(BaseModel):
#     email_otp: OTP_CODE_FIELD
#
# class RegistrationSendOTPResponse(BaseResponseSchema):
#     email_id: str
#     email_expire_at: datetime
