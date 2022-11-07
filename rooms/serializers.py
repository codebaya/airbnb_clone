from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from categories.serializers import TinyCategorySerializer
from medias.serializers import PhotoSerializer
from users.serializers import TinyUserSerializer
from wishlists.models import Wishlist
from .models import Amenity, Room


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name", "description",
        )


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    # amenities = AmenitySerializer(read_only=True, many=True)
    category = TinyCategorySerializer(read_only=True, )

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        print(self.context)
        return room.rating()

    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context['request']
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()


def create(self, validated_data):
    # 	print(validated_data)
    return


# return super().create(validated_data)


# return Room.objects.create(**validated_data)


class RoomListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk", "name", "country", "city", "price", "rating", "is_owner", "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user
