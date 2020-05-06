
import json

from rest_framework import views, status
from django.http import HttpResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from url_filter.integrations.drf import DjangoFilterBackend

from authentication.models import AuthUser
from user_management.middlewares.authentication import RegisterTokenAuthentication, FetchTokenAuthentication
from authentication.serializers import OTPSerializer, JWTObtainPairSerializer, JWTRefreshSerializer, JWTVerifySerializer


class OTPView(CreateAPIView):
    """
    View to provide OTP functionality
    """
    serializer_class = OTPSerializer


class JWTObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = JWTObtainPairSerializer
    authentication_classes = [FetchTokenAuthentication]


class JWTRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = JWTRefreshSerializer


class JWTVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    serializer_class = JWTVerifySerializer


class RegisterView(TokenViewBase):
    """
    Register a new user
    """
    serializer_class = JWTObtainPairSerializer
    authentication_classes = [RegisterTokenAuthentication]
