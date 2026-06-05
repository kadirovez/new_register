
from src.services.auth.registration.validate_personal_information import validate_personal_information
from src.services.auth.registration.send_email_otp import send_email_otp
from src.services.auth.registration.confirm_email_otp import confirm_email_otp
from src.services.auth.registration.complete_registration import complete_registration
from src.services.auth.registration.confirm_password import confirm_password
from src.services.auth.registration.validate_password import validate_password
from src.services.auth.registration.cancel_registration import cancel_registration


class RegistrationServices:
    ''' Service for registration flow operations '''

    complete_registration = complete_registration,
    confirm_email_otp = confirm_email_otp,
    confirm_password = confirm_password,
    send_email_otp = send_email_otp,
    validate_personal_information = validate_personal_information,
    validate_password = validate_password
    cancel_registration = cancel_registration


registration_service = RegistrationServices()
