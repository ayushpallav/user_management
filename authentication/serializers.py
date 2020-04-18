from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import serializers

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
