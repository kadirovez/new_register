
from typing import Annotated
from datetime import datetime

from pydantic import Field, BeforeValidator, AfterValidator, EmailStr

from src.core.settings import settings
from src.utils.normalize import  normalize_lowercase

from src.utils.validator import validate_password_policy

USERNAME_FIELD = Annotated[
    str,
    Field(
        ...,
        min_length=3,
        max_length=32,
        description='Username'
    ),
    BeforeValidator(normalize_lowercase)
]

NAME_FIELD = Annotated[
    str,
    Field(
        ...,
        min_length=2,
        max_length=32,
        pattern=r"^[a-zA-Z]+$",
        description='Name'
    )
]

PASSWORD_FIELD = Annotated[
    str,
    Field(
        ...,
        min_length=settings.password_min_length,
        max_length=255,
        description='Password'
    ),
    AfterValidator(validate_password_policy)
]

EMAIL_FIELD = Annotated[
    EmailStr,
    Field(
        ...,
        max_length=255,
        description='Email address'
    )
]


OTP_CODE_FIELD = Annotated[
    str,
    Field(
        ...,
        min_length=4,
        max_length=4,
        pattern=r"^\d{6}$",
        description='4-digit OTP code'
    )
]

TOTP_CODE_FIELD = Annotated[
    str,
    Field(
        ...,
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
        description='6-digit TOTP code'
    )
]
