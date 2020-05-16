import re, uuid, jwt, json
from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from django.conf import settings

from authentication.models import AuthUser
from authentication.constants import JWTConstants, ExceptionMessages
from authentication.utils import _2FactorOTP

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details
    """
    uuidt = serializers.CharField(read_only=True)

    def create(self, validated_data):
        validated_data['uuidt'] = uuid.uuid4().hex
        validated_data['password'] = make_password(get_random_string())
        JWTObtainPairSerializer(data=validated_data)
        return super().create(validated_data)

    class Meta:
        model = AuthUser
        fields = ('__all__')
        extra_kwargs = {
            "password": {"write_only": True},
            "is_superuser": {"write_only": True},
            "is_staff": {"write_only": True},
            "groups": {"write_only": True},
            "user_permissions": {"write_only": True}
        }


class OTPSerializer(serializers.Serializer):
    username = serializers.CharField()
    session_id = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            session_id = _2FactorOTP(
                phone_number=validated_data["username"]
            ).send_otp()
        except:
            raise Exception(ExceptionMessages.OTP_NOT_SENT)
        validated_data['session_id'] = session_id
        return validated_data


class JWTAuthenticationSerializer(serializers.Serializer):
    username_field = UserModel.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not self.user:
            _user = UserSerializer(data=self.context['request'].data)
            if _user.is_valid():
                self.user = _user.save()
            else:
                raise AuthenticationFailed(
                    'No account found with the given credentials'
                )

        return {}


    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `JWTAuthenticationSerializer` subclasses')

    @classmethod
    def ask_to_signup(cls, username):
        """
        If user not registered, ask to get
        signed up
        """
        payload = {
            "issue_time": int(datetime.now().strftime('%s')),
            "username": username
        }
        return {
            "registered": False,
            "token": jwt.encode(payload, settings.SECRET_KEY),
            "username": username,
            "required_fields": AuthUser.REQ_FIELDS
        }


class JWTObtainPairSerializer(JWTAuthenticationSerializer):
    """
    There can be two cases:
    - The username exists: It is a login attempt -> return corresponding token and all user details
    - The username does not exist: It is a phone number verification for a new user -> give a one time token
                                   and ask for signing up
    """
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            return self.ask_to_signup(self.context['request'].data.get('username'))

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['uuidt'] = self.user.uuidt

        return data


class JWTRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)

        return data


class JWTVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        UntypedToken(attrs['token'])

        return {}
