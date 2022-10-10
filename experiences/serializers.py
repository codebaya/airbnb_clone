from rest_framework.serializers import ModelSerializer

from experiences.views import Perk


class PerkSerializer(ModelSerializer):
	
	class Meta:
		model = Perk
		fields = "__all__"