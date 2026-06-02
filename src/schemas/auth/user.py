
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):

    username : str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-z0-9]+$",
        description='Username'
    )

    first_name : str = Field(
        ...,
        min_length=3,
        max_length=50,
        description='First Name'
    )

    last_name : str = Field(
        ...,
        min_length=3,
        max_length=50,
        description='Last Name'
    )

    password : str = Field(
        ...,
        min_length=8,
        max_length=255,
        description='Password'
    )

    email : str = Field(
        ...,
        max_length=255,
        description='Email address'
    )

    email_is_confirmed: Optional[bool] = Field(
        False,
        description="Email is confirmed."
    )

class UserUpdate(BaseModel):

    password: Optional[str] = None
    bad_password_count: Optional[int] = None
    bad_email_code_count: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr = None
    email_is_confirmed: Optional[bool] = None
    email_code_limit: Optional[int] = None
    is_active: Optional[bool] = None
    is_locked: Optional[bool] = None
