from rest_framework import serializers

from authentication.models import UserDetail


class UserDetailSerializer(serializers.ModelSerializer):
	"""
	Serializer to for user data
	"""
	class Meta:
		model = UserDetail
		fields = ('__all__')
