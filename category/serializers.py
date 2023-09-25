from rest_framework import serializers
from .models import CategoryModel
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=CategoryModel
        fields=("id","title","parent")

    def validate(self, attrs):
        category=CategoryModel.objects.filter(title=attrs["title"],parent=attrs["parent"]).first()
        if category:
            raise serializers.ValidationError("Name already exists by this parent!")
        return attrs

