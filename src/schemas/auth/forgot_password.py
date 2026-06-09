
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.schemas.base import BaseResponseSchema
from src.schemas.fields import USERNAME_FIELD, EMAIL_FIELD, OTP_CODE_FIELD, PASSWORD_FIELD


class ForgotPasswordLoginRequest(BaseModel):
    ''' Forgot password identifier request '''

    login: str

class ForgotPasswordUsernameRequest(BaseModel):
    ''' Forgot password username request '''

    username: USERNAME_FIELD


class ForgotPasswordEmailRequest(BaseModel):
    ''' Forgot password email request '''

    email: EMAIL_FIELD


class ForgotPasswordEmailOTPRequest(BaseModel):
    ''' Forgot password email OTP request '''

    email_otp: OTP_CODE_FIELD


class ForgotPasswordNewPasswordRequest(BaseModel):
    ''' Forgot password new password request '''

    new_password: PASSWORD_FIELD


class ForgotPasswordNewPasswordConfirmRequest(BaseModel):
    ''' Forgot password new password confirmation '''

    password_confirm: PASSWORD_FIELD

class ForgotPasswordMaskedEmailResponse(BaseResponseSchema):
    ''' Masked email response '''

    masked_email: str


class ForgotPasswordUpdate(BaseModel):
    ''' Update forgot password schema '''

    login_method: Optional[str] = None
    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    new_password: Optional[str] = None
    new_password_is_validated: Optional[bool] = None
    new_password_is_confirmed: Optional[bool] = None
    email_matched: Optional[bool] = None
    email_is_confirmed: Optional[bool] = None
    email_code_sent: Optional[str] = None
    email_code_id: Optional[str] = None
    email_code_expire_at: Optional[datetime] = None
    is_completed: Optional[bool] = None

