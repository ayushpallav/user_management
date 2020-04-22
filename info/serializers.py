from rest_framework import serializers

from authentication.models import UserDetail


class UserDetailSerializer(serializers.ModelSerializer):
	"""
	Serializer to for user data
	"""
	first_name = serializers.SerializerMethodField()
	last_name = serializers.SerializerMethodField()

	def get_first_name(self, obj):
		return obj.user.first_name

	def get_last_name(self, obj):
		return obj.user.last_name

	class Meta:
		model = UserDetail
		fields = ('__all__')
