
from src.services.auth.login.cancel_login import cancel_login
from src.services.auth.login.complete_login import complete_login
from src.services.auth.login.confirm_email import confirm_email
from src.services.auth.login.confirm_email_otp import confirm_email_otp
from src.services.auth.login.send_email_otp import send_email_otp
from src.services.auth.login.validate_email import validate_email
from src.services.auth.login.validate_identifier import validate_identifier
from src.services.auth.login.validate_password import validate_password
from src.services.auth.login.validate_username import validate_username

class LoginServices:

    validate_username = validate_username
    validate_email = validate_email
    validate_identifier = validate_identifier
    validate_password = validate_password
    confirm_email = confirm_email
    send_email_otp = send_email_otp
    confirm_email_otp = confirm_email_otp
    complete_login = complete_login
    cancel_login = cancel_login


# Singleton instance 
login_service = LoginServices()