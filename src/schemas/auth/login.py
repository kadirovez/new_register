
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from src.schemas.fields import USERNAME_FIELD, EMAIL_FIELD, PASSWORD_FIELD, OTP_CODE_FIELD

class LoginUsernameRequest(BaseModel):
    username : USERNAME_FIELD

class LoginPasswordRequest(BaseModel):
    password : PASSWORD_FIELD

class LoginEmailRequest(BaseModel):
    email : EMAIL_FIELD

class LoginEmailOTPRequest(BaseModel):
    email_otp : OTP_CODE_FIELD

class LoginUpdate(BaseModel):
    # user_id: Optional[int] = None
    username : Optional[str] = None
    email: Optional[str] = None
    email_code_sent: Optional[str] = None
    email_code_id: Optional[str] = None
    email_code_expire_at: Optional[datetime] = None
    email_code_is_confirmed: Optional[bool] = None
    is_completed: Optional[bool] = None
