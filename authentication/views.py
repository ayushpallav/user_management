
import json
from rest_framework import views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.models import UserDetail
from authentication.serializers import UserSerializer


class AuthView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if not user.is_valid():
            return Response(
              json.dumps({'Error': "Invalid credentials"}),
              status=400,
              content_type="application/json"
            )
        user.save()
        return super().post(request, *args, **kwargs)

