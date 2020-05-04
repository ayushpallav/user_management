import jwt
import requests
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import resolve
from rest_framework import status, authentication, exceptions

from authentication.utils import _2FactorOTP

UserModel = get_user_model()


class RegisterTokenAuthentication(authentication.BaseAuthentication):
    """
    Check if the incoming request is to create a new user
    aka, sign up request
    """

    def is_valid_token(self, token=None, body=None):
        now = int(datetime.now().strftime("%s"))
        def _valid_time(time):
            if now - time < settings.SIGNUP_TOKEN_VALIDITY:
                return (True, '')
            return (False, 'token_expired')
        if not token or not body:
            return (False, 'token_not_found')
        decrypted_payload = jwt.decode(token, settings.SECRET_KEY)
        username, issue_time = decrypted_payload.get('username'), decrypted_payload.get('issue_time')
        if UserModel.objects.filter(username=username).exists():
            return (False, 'Gandu registered h tu already')
        if username != body.get('username'):
            return (False, 'username not matching with the token')
        return _valid_time(issue_time)

    def authenticate(self, request):
        """
        We authorize the given token with user-management.
        """

        extempted_urls = []
        if resolve(request.path_info).url_name in extempted_urls:
            return (None, None)

        auth_token = request.META.get('HTTP_AUTHORIZATION')
        valid, reason = self.is_valid_token(token=auth_token, body=request.data)
        if not valid:
            raise exceptions.AuthenticationFailed(
                reason
            )

        return (None, None)

    def authenticate_header(self, request):
        return 'Token'


class FetchTokenAuthentication(authentication.BaseAuthentication):
    """
    To authenticate for /token path:
    /token:
    - returns relevant token if user already registered
    - asks new user to register first if valid OTP provided and
    """

    def authenticate(self, request):
        # if user exists-> validate
        username, otp, session_id = request.data.get("username", ""), request.data.get("otp"), request.data.get("session_id")
        if not username:
            raise exceptions.ParseError(
                {"username": "Is a required field"}
            )
        # if user not there-> check for validity of OTP
        if not otp or not session_id:
            raise exceptions.AuthenticationFailed(
                "otp and session_id both are required for a user to get access token"
            )
        if _2FactorOTP(username).verify_otp(
            otp=otp,
            session_id=session_id
        ):
            return (None, None)
        raise exceptions.AuthenticationFailed(
            "OTP expired"
        )
