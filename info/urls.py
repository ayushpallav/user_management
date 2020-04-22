from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from info.views import UserDetailView

router = routers.DefaultRouter()
router.register(r'user', UserDetailView)


urlpatterns=[
	url('/', include(router.urls)),
]
