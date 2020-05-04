import requests
from django.conf import settings

from authentication.constants import _2FConstants


class _2FactorOTP:
    """
    To handle all processing related to 2Factor OTP
    service
    """
    def __init__(self, phone_number, *args, **kwargs):
        self.phone_number = phone_number

    def send_otp(self):
        url = settings.OTP_BASE_URL + _2FConstants.SEND_OTP_URL_PATH.format(
            api_key=settings.OTP_API_KEY, phone_number=self.phone_number
        )
        try:
            response = requests.get(url)
        except:
            raise Exception
        data = response.json()
        return data.get("Details")

    def verify_otp(self, session_id, otp):
        url = settings.OTP_BASE_URL + _2FConstants.VERIFY_OTP_URL_PATH.format(
            api_key=settings.OTP_API_KEY, session_id=session_id, otp=otp
        )
        try:
            response = requests.get(url)
        except:
            raise Exception
        print(response.json())
        if response.json().get("Details")=="OTP Matched":
            return True
        return False
