from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from bookings.models import Booking
from experiences.models import Experience
from experiences.views import Perk
from users.serializers import TinyUserSerializer


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        # fields = "__all__"
        fields = "pk", "name", "price", "host", "description", "perks",


class ExperienceDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    category = TinyUserSerializer(read_only=True)
    perks = PerkSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = "__all__"


class CreateExperienceBookingSerializer(ModelSerializer):
    experience_date = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "experience_time", "guests",
        )

    def validate_experience_date(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        return value

    def validate(self, data):
        if Booking.objects.filter(
                experience_date=data["experience_time"]
        ).exists():
            raise serializers.ValidationError(
                "Those dates are already taken."
            )
        return data
