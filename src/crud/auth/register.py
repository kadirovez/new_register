
from src.crud.auth.base import CRUDSessionBase
from src.models.auth.register_session import Registration
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.auth.registration import RegistrationUpdate


class CRUDRegistration(CRUDSessionBase[Registration, CreateSessionSchema, RegistrationUpdate]):
    reset_values = {
        "username": None,
        "first_name": None,
        "last_name": None,
        "email": None,
        "password": None,
        "password_is_confirmed": False,
        "is_completed": False,
    }


registration_crud = CRUDRegistration(Registration)
