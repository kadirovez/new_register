
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.register import registration_crud
from src.crud.auth.user import user_crud
from src.models.auth.register_session import Registration
from src.schemas import UserCreate
from src.schemas.auth.registration import RegistrationCompleteResponse, RegistrationUpdate


async def complete_registration(
        db: AsyncSession,
        registration_session: Registration,
):
    ''' Completes registration and creates user in database '''

    if registration_session.is_completed:
        raise HTTPException(
            status_code=401,
            detail='Session already completed'
        )

    if registration_session.email_is_confirmed and registration_session.password_is_confirmed:
        await registration_crud.update(
            db=db,
            db_obj=registration_session,
            obj_in=RegistrationUpdate(
                is_completed=True
            )
        )
    else:
        raise HTTPException(
            status_code=401,
            detail='Something went wrong'
        )


    # Creates user from register session
    await user_crud.create(
        db=db,
        obj_in=UserCreate(
            username=registration_session.username,
            first_name=registration_session.first_name,
            last_name=registration_session.last_name,
            password=registration_session.password,
            email=registration_session.email,
            email_is_confirmed=registration_session.email_is_confirmed,
            is_active=registration_session.is_active
        )
    )



