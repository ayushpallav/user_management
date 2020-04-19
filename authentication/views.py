
import json
from rest_framework import views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

from authentication.models import UserDetail
from authentication.serializers import UserSerializer


class AuthView(TokenObtainPairView):
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
        user.save()
        render = super().post(request, *args, **kwargs)
        obj = User.objects.filter(
            username=user.data.get('username'),
            email=user.data.get('email')
        ).first()
        render.data['user_id'] = obj.id
        return render
