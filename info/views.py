from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import CreateAPIView
from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework.response import Response

from authentication.models import AuthUser
from info.serializers import UserDetailSerializer, UserDetailBulkSerializer


class UserDetailView(ModelViewSet):
    """
    Model view to return user details
    corresponding to uuidt
    """
    queryset = AuthUser.objects.all()
    serializer_class = UserDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['uuidt', 'phone_number']


class UserDetailBulk(CreateAPIView):
    """
    returns all user details
    for the list of uuidts
    """
    queryset = AuthUser.objects.all()
    serializer_class = UserDetailBulkSerializer
