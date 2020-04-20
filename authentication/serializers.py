import re

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import UserDetail


class UserSerializer(serializers.Serializer):
    """
    Serializer for user details
    """
    username = serializers.CharField()
    address = serializers.CharField()
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def validate_phone_number(self, phone_number):
        if not re.match('^.{10}$', phone_number):
            raise ValidationError({"phone_number": "invalid phone number"})
        return phone_number

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user_id = user.save()
        UserDetail.objects.create(
            user_id=user.id,
            address=validated_data["address"],
            phone_number=validated_data["phone_number"]
        )
        return validated_data
