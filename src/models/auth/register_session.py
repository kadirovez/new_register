
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String

from src.models.auth.base import SessionAuthDataBase


class Registration(SessionAuthDataBase):
    """
    Temporary registration session.

    Flow: profile (name, username, email) -> password -> confirm password -> finish.
    """

    __tablename__ = "registration"

    username: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(32),
        nullable=False,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=False,
    )

    password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=False,
    )

    password_is_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default="false",
    )

    # --- Not used in current registration flow (no email OTP on register) ---
    # email_is_confirmed: Mapped[bool] = mapped_column(
    #     Boolean,
    #     default=False,
    #     nullable=False,
    #     server_default="false",
    # )
    # email_code_limit: Mapped[int] = mapped_column(
    #     Integer,
    #     default=settings.session_email_code_limit,
    #     nullable=False,
    #     server_default="0",
    # )
    # email_code_sent: Mapped[bool] = mapped_column(
    #     Boolean,
    #     default=False,
    #     nullable=False,
    #     server_default="false",
    # )
    # email_code_id: Mapped[str | None] = mapped_column(
    #     String(32),
    #     nullable=True,
    # )
    # email_code_expire_at: Mapped[datetime | None] = mapped_column(
    #     DateTime,
    #     default=None,
    #     nullable=True,
    # )
