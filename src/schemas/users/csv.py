
from pydantic import BaseModel, Field

from src.schemas.fields import USERNAME_FIELD, NAME_FIELD, EMAIL_FIELD, PASSWORD_FIELD


class UserCsvImportRow(BaseModel):
    ''' One row from users import CSV '''

    username: USERNAME_FIELD
    first_name: NAME_FIELD
    last_name: NAME_FIELD
    email: EMAIL_FIELD
    password: PASSWORD_FIELD
    email_confirmed: bool = Field(default=False)
    is_active: bool = Field(default=True)


class UserImportResponse(BaseModel):
    ''' Result of CSV import '''

    created: int
    skipped: int
    errors: list[str]
