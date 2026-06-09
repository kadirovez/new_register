
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.forgot_password import forgot_password_crud
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.auth.forgot_password import (
    ForgotPasswordLoginRequest,
    ForgotPasswordEmailRequest,
    ForgotPasswordUpdate,
    ForgotPasswordUsernameRequest,
)
from src.services.auth.forgot_password.validate_email import validate_email
from src.services.auth.forgot_password.validate_username import validate_username


async def validate_identifier(
        db: AsyncSession,
        forgot_password_session: ForgotPassword,
        obj_in: ForgotPasswordLoginRequest,
):
    # Check for login method
    identifier = obj_in.login.strip().lower()

    try:
        email_obj = ForgotPasswordEmailRequest(email=identifier)
        await forgot_password_crud.update(
            db=db,
            id=forgot_password_session.id,
            obj_in=ForgotPasswordUpdate(
                login_method='email'
            ),
        )
        forgot_password_session.login_method = 'email'
        return await validate_email(
            db=db,
            forgot_password_session=forgot_password_session,
            obj_in=email_obj,
        )

    except ValidationError:
        username_obj = ForgotPasswordUsernameRequest(username=identifier)
        await forgot_password_crud.update(
            db=db,
            id=forgot_password_session.id,
            obj_in=ForgotPasswordUpdate(
                login_method='username'
            ),
        )
        forgot_password_session.login_method = 'username'
        return await validate_username(
            db=db,
            forgot_password_session=forgot_password_session,
            obj_in=username_obj,
        )
