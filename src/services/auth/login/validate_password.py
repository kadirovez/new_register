
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.auth.login import login_crud
from src.crud.auth.user import user_crud
from src.models.auth.login_session import Login
from src.schemas import LoginPasswordRequest, UserUpdate, LoginUpdate, LoginMaskedEmailResponse
from src.schemas.base import StatusResponseSchema
from src.utils.mask_email import mask_email
from src.utils.password import verify_password


async def validate_password(
        self,
        db: AsyncSession,
        login_session: Login,
        obj_in: LoginPasswordRequest,
):

   if not login_session.user_id:
       raise HTTPException(
           status_code=401,
           detail='User id not found'
       )

   await login_crud.reset(
       db=db,
       db_obj=login_session,
       keep_fields={
           'user_id' : True,
           'username' : True,
           'email' : True,
       }
   )

   user = await user_crud.get(
       db=db,
       id=login_session.user_id,
   )
   if not user:
       raise HTTPException(
           status_code=401,
           detail='User not found'
       )

   if not verify_password(obj_in.password, user.password):
       bad_password_time = datetime.now(timezone.utc)
       bad_password_count = user.bad_password_count + 1
       if bad_password_count > settings.user_bad_password_limit:
           await user_crud.update(
               db=db,
               id=user.id,
               obj_in=UserUpdate(
                   bad_password_time=bad_password_time,
                   bad_password_count=bad_password_count,
                   is_locked=True
               )
           )
           raise HTTPException(
               status_code=401,
               detail='Too many attempts')
       await user_crud.update(
           db=db,
           id=user.id,
           obj_in=UserUpdate(
               bad_password_count=bad_password_count,
               bad_password_time=bad_password_time,
           )
       )
       raise HTTPException(
           status_code=401,
           detail='Invalid password'
       )

   await user_crud.update(
       db=db,
       id=user.id,
       obj_in=UserUpdate(
           bad_password_count=0,
           bad_password_time=None,
       )
   )

   await login_crud.update(
       db=db,
       id=login_session.id,
       obj_in=LoginUpdate(
           password_is_validated = True
       )
   )

   return LoginMaskedEmailResponse(
       masked_email = mask_email(user.email)
   )










