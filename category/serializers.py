from rest_framework import serializers
from .models import CategoryModel
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=CategoryModel
        fields=("id","title","parent")

    def validate(self, attrs):
        title=CategoryModel.objects.filter(title=attrs["title"]).first()
        print(attrs["parent"])
        if title :
            raise serializers.ValidationError("Name already exists!")
        return attrs

