import re

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
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

    def validate_password(self, password):
        if not re.match('^(?=.*\d).{4,8}$', password):
            raise ValidationError({"password": "Password must be between 4 and 8 digits long and include at least one numeric digit."})
        return password

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        try:
            user_id = user.save()
        except IntegrityError:
            pass
        else:
            UserDetail.objects.create(
                user_id=user.id,
                address=validated_data["address"],
                phone_number=validated_data["phone_number"]
            )
        return validated_data
