from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from info.views import UserDetailView, UserDetailBulk

router = routers.DefaultRouter()
router.register(r'user', UserDetailView)


urlpatterns=[
	path('/bulk_retrieve', UserDetailBulk.as_view(), name='bulk'),
	url('/', include(router.urls)),
]
