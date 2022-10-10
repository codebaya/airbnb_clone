from rest_framework.serializers import ModelSerializer

from categories.serializers import TinyCategorySerializer
from users.serializers import TinyUserSerializer
from .models import Amenity, Room


class AmenitySerializer(ModelSerializer):
	class Meta:
		model = Amenity
		fields = (
			"name", "description",
		)


class RoomDetailSerializer(ModelSerializer):
	
	owner = TinyUserSerializer()
	amenities = AmenitySerializer(many=True)
	category = TinyCategorySerializer()
	class Meta:
		model = Room
		fields = "__all__"


class RoomListSerializer(ModelSerializer):
	class Meta:
		model = Room
		fields = (
			"pk", "name", "country", "city", "price",
		)