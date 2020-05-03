import jwt
import requests
from datetime import datetime

from django.conf import settings
from django.urls import resolve
from rest_framework import status, authentication, exceptions


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
