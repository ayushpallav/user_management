
class AuthConstants:
    """
    Constants relevant to AuthUser/AuthGroups etc.
    """
    END_USER = "end_user"
    STAFF = "staff"
    USERNAME = "username"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"
    SOCIETY = "society"
    FLAT = "flat"
    FLOOR = "floor"
    TOWER = "tower"
    PHONE_NUMBER = "phone_number"


class JWTConstants:
    SIGNUP_EVENT = "No user found for given username, register using the one time token provided"


class _2FConstants:
    SEND_OTP_URL_PATH = "/{api_key}/SMS/+91{phone_number}/AUTOGEN/OTPLOGIN"
    VERIFY_OTP_URL_PATH = "/{api_key}/SMS/VERIFY/{session_id}/{otp}"


class ExceptionMessages:
    OTP_NOT_SENT = "Not able to send OTP"
