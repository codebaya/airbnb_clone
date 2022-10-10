from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Category
		fields = "__all__"


class TinyCategorySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Category
		fields = (
			"name", "kind",
		)