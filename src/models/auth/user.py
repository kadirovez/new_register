
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.settings import settings
from src.models.base import BaseDataModel
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.auth.login_session import Login

class User(BaseDataModel):

    __tablename__ = 'user'

    username : Mapped[str] = mapped_column(
        String(32),
        unique=True,
        Nullable=False,
        index=True
    )

    first_name : Mapped[str] = mapped_column(
        String(32),
        Nullable=False,
        index=True
    )

    last_name : Mapped[str] = mapped_column(
        String(32),
        Nullable=False,
        index=True
    )

    # Email
    email : Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    email_confirmed : Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default='false'
    )

    email_code_limit : Mapped[int] = mapped_column(
        default=settings.user_email_code_limit,
        nullable=False
    )

    bad_email_code_time : Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True
    )

    # Password
    password : Mapped[int] = mapped_column(
        String(255),
        nullable=False
    )

    password_change : Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True
    )

    bad_password_count : Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )

