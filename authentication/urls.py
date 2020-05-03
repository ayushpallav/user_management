from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from authentication.views import JWTObtainPairView, JWTRefreshView, JWTVerifyView, RegisterView


urlpatterns=[
	path('token/', JWTObtainPairView.as_view(), name='get_token'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', JWTRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', JWTVerifyView.as_view(), name='token_verify'),
]
