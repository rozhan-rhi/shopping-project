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




# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model=CategoryModel
#         fields=("id","title")
#
#     def validate(self, attrs):
#         category=CategoryModel.objects.filter(title=attrs["title"]).first()
#         if category:
#             raise serializers.ValidationError("Name already exists!")
#         return attrs
#
#
# class SubCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model=SubCategoryModel
#         fields=("id","name","category")
#
#     def create(self, validated_data):
#         # print(validated_data)
#         # category=CategoryModel.objects.filter(title=validated_data["category"]).first()
#         try:
#             subcategory=SubCategoryModel.objects.filter(name=validated_data["name"],category=validated_data["category"]).first()
#             print(subcategory)
#             if subcategory==None:
#                 print("none")
#                 return SubCategoryModel.objects.create(**validated_data)
#                 print("ok")
#                 # return newSubcategory
#                 #     raise serializers.ValidationError("Name already not exists by this parent!")
#             # else:
#
#                 return instance
#             return validated_data
#
#         except Exception as e:
#             print(e)
#             newSubcategory = SubCategoryModel.objects.create(**validated_data)
#             return newSubcategory



 # {
 #        "name": "iphone",
 #        "category": 2
 #    }