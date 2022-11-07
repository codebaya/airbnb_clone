from rest_framework.serializers import ModelSerializer

from users.models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name", "avatar", "username",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password", "id", "is_staff", "is_superuser",
            "first_name", "last_name", "groups",
            "user_permissions", "is_active",)
