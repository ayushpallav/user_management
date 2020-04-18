from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from authentication.views import AuthView


urlpatterns=[
	path('token/', AuthView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
