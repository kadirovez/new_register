
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Boolean, String

from src.models.base import BaseDataModel
from src.core.settings import settings

import datetime


class Registration(BaseDataModel):


    __tablename__ = 'registration'

    # User info
    username : Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )

    first_name : Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )

    last_name : Mapped[str] = mapped_column(
        String(32),
        nullable=True
    )

    # Password info
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

    # Email info
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

    email_code_limit : Mapped[int] = mapped_column(
        default=settings.session_email_code_limit,
        nullable=False,
        server_default='0'
    )

    email_code_sent : Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false'
    )
    email_code_id : Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )

    email_code_expire_at : Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True
    )
