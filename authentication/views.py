
import json
from rest_framework import views
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate

from url_filter.integrations.drf import DjangoFilterBackend

from authentication.models import UserDetail
from authentication.serializers import UserSerializer


class SignUpView(TokenObtainPairView):
    """
    Generate a access and refresh token with given payload
    Parameters needed (all mandatory)
    - username: string
    - address: string
    - phone_number: string (10 digit number)
    - first_name: string
    - last_name: string
    - email: string (email validation)
    - password: string (4-8 characters)
    """

    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if not user.is_valid():
            return Response(
              json.dumps({'Error': "Invalid Payload"}),
              status=400,
              content_type="application/json"
            )
        try:
            user_obj = user.save()
        except IntegrityError:
            raise ValidationError({"user": "Listen Morty! The user already exists, log in instead"})
        render = super().post(request, *args, **kwargs)
        render.data['uuidt'] = user_obj.get('uuidt')
        return render


class LoginView(TokenObtainPairView):
    """
    Generate a access and refresh token with given payload
    Parameters needed (all mandatory)
    - username: string
    - address: string
    - phone_number: string (10 digit number)
    - first_name: string
    - last_name: string
    - email: string (email validation)
    - password: string (4-8 characters)
    """

    def post(self, request, *args, **kwargs):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if not user:
            return HttpResponse('{"user": "Listen Morty! The username/password you have entered is invalid"}', status=401)
        render = super().post(request, *args, **kwargs)
        obj = UserDetail.objects.filter(user_id=user.id).first()
        render.data['uuidt'] = obj.uuidt
        return render
