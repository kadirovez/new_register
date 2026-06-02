
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime

from src.models.base import BaseDataModel

import datetime


class Login(BaseDataModel):

    __tablename__ = 'login'

    # User info
    username : Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )

    # Password
    password : Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    password_is_confirmed : Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false'
    )

    password_is_validated : Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false'
    )

    # Email

    email : Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email_is_confirmed : Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false'
    )

    email_code_sent : Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )

    email_code_id : Mapped[str | None] = mapped_column(
        String(32),
        nullable=True
    )

    email_code_expire_at : Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True
    )

    # TOTP fields

    totp_code_is_confirmed : Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false'
    )

    totp_token : Mapped[str] = mapped_column(
        String(32),
        nullable=True
    )

