
from src.services.auth.forgot_password.cancel_forgot_password import cancel_forgot_password_session
from src.services.auth.forgot_password.change_password import change_password
from src.services.auth.forgot_password.complete_forgot_password import complete_forgot_password
from src.services.auth.forgot_password.confirm_email import confirm_email
from src.services.auth.forgot_password.confirm_password import confirm_password
from src.services.auth.forgot_password.send_email_otp import  forgot_password_send_email_otp
from src.services.auth.forgot_password.validate_email_otp import validate_email_otp
from src.services.auth.forgot_password.validate_email import validate_email
from src.services.auth.forgot_password.validate_identifier import validate_identifier
from src.services.auth.forgot_password.validate_username import validate_username


class ForgotPasswordServices:
    cancel_forgot_password = staticmethod(cancel_forgot_password_session)
    change_password = staticmethod(change_password)
    complete_forgot_password = staticmethod(complete_forgot_password)
    confirm_password = staticmethod(confirm_password)
    confirm_email = staticmethod(confirm_email)
    forgot_password_send_email_otp = staticmethod(forgot_password_send_email_otp)
    validate_email_otp = staticmethod(validate_email_otp)
    validate_email = staticmethod(validate_email)
    validate_identifier = staticmethod(validate_identifier)
    validate_username = staticmethod(validate_username)


forgot_password_service = ForgotPasswordServices()
