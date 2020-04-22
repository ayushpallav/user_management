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


class UserDetailBulkSerializer(serializers.Serializer):
	"""
	Serializer to return data corresponding to the list of
	uuidts provided
	"""
	uuidts = serializers.ListField(
		child=serializers.UUIDField(),
		write_only=True
	)
	data = serializers.ListField(
		child=serializers.JSONField(),
		read_only=True
	)

	def create(self, validated_data):
		validated_data['data'] = [
			{
				"uuidt": str(x.uuidt),
				"society": x.society,
				"flat": x.flat,
				"floor": x.floor
			}
			for x in list(
				UserDetail.objects.filter(uuidt__in=validated_data["uuidts"])
			)
		]
		return validated_data
