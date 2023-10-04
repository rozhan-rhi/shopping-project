from rest_framework import serializers
from .models import CategoryModel,SubCategoryModel
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=CategoryModel
        fields=("id","title")

    def validate(self, attrs):
        category=CategoryModel.objects.filter(title=attrs["title"]).first()
        if category:
            raise serializers.ValidationError("Name already exists!")
        return attrs


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategoryModel
        fields=("id","name","category")

    def create(self, validated_data):
        print(validated_data)
        category=CategoryModel.objects.filter(title=validated_data["category"]).first()
        subcategory=SubCategoryModel.objects.filter(name=validated_data["name"],category=category.id).first()
        # validated_data['category']=category.id
        if subcategory:
            raise serializers.ValidationError("Name already exists by this parent!")
        newSubcategory=SubCategoryModel.objects.create(**validated_data)
        return newSubcategory