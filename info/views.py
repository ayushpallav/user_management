from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from url_filter.integrations.drf import DjangoFilterBackend

from authentication.models import UserDetail
from info.serializers import UserDetailSerializer


class UserDetailView(ModelViewSet):
    """
    Model view to return user details
    corresponding to uuidt
    """
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['uuidt']
