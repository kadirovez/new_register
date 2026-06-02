
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.schemas.base import BaseResponseSchema
from src.schemas.fields import USERNAME_FIELD, NAME_FIELD, PASSWORD_FIELD, EMAIL_FIELD, OTP_CODE_FIELD


class RegistrationUsernameRequest(BaseModel):
    username : USERNAME_FIELD

class RegistrationPasswordRequest(BaseModel):
    password : PASSWORD_FIELD

class RegistrationPasswordConfirm(BaseModel):
    confirm_password : PASSWORD_FIELD

class RegistrationPersonalInformation(BaseModel):
    first_name : NAME_FIELD
    last_name : NAME_FIELD

class RegistrationEmailRequest(BaseModel):
    email : EMAIL_FIELD

class RegistrationEmailOTPRequest(BaseModel):
    email_otp : OTP_CODE_FIELD

class RegistrationSendOTPResponse(BaseResponseSchema):
    email_id : str
    email_expire_at : datetime

class RegistrationUpdateBaseModel(BaseModel):
    username : Optional[str] = None
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    password : Optional[str] = None
    password_is_confirmed : Optional[bool] = None
    email : Optional[str] = None
    email_is_confirmed : Optional[bool] = None
    email_code_limit : Optional[int] = None
    email_code_id : Optional[str] = None
    email_code_sent : Optional[str] = None
    email_code_expire_at : Optional[str] = None
    is_completed : Optional[bool] = None


