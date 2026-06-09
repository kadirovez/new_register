
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.auth.base import SessionDatabaseModel

if TYPE_CHECKING:
    from src.models.auth.user import User

class ForgotPassword(SessionDatabaseModel):
    ''' Forgot password model '''

    __tablename__ = 'forgot_password'

    login_method : Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    user_id : Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    username : Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        index=True,
    )

    email : Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        index=True,
    )

    email_is_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default='false'
    )

    email_matched : Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false',
    )

    email_code_sent : Mapped[str | None] = mapped_column(
        String(256),
        nullable=True,
    )

    email_code_id : Mapped[str | None] = mapped_column(
        String(256),
        nullable=True,
    )

    email_code_expire_at : Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True
    )

    new_password : Mapped[str | None] = mapped_column(
        String(256),
        nullable=True
    )

    new_password_is_confirmed : Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default='false'
    )

