
from src.crud.auth.base import CRUDSessionBase
from src.models.auth.forgot_password_session import ForgotPassword
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.auth.forgot_password import ForgotPasswordUpdate


class CRUDForgotPassword(CRUDSessionBase[ForgotPassword, CreateSessionSchema, ForgotPasswordUpdate]):
    ''' CRUD operations for forgot password session '''

    reset_values = {
        'login_method': None,
        'user_id': None,
        'username': None,
        'email': None,
        'new_password': None,
        'new_password_validated': False,
        'new_password_is_confirmed': False,
        'email_code_sent': None,
        'email_is_matched': False,
        'email_code_id': None,
        'email_is_confirmed': False,
        'email_code_expires_at': None,
        'is_completed': False
    }

forgot_password_crud = CRUDForgotPassword(ForgotPassword)
