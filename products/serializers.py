from rest_framework import serializers
from .models import ProductModel,ChartModel
from category.serializers import CategorySerializer
from category.models import CategoryModel

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields=('id','title','description','current_price','thumbnail')



class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields='__all__'
        extra_kwargs = {
            "thumbnail": {"write_only": True}
        }


    def create(self, validated_data):
        product = ProductModel.objects.filter(title=validated_data["title"], category=validated_data["category"]).first()
        if product:
            raise serializers.ValidationError("there is a same product with this category!")
        newProduct=ProductModel.objects.create(**validated_data)
        return newProduct

    def update(self, instance, validated_data):
        instance.title =validated_data.get("title",instance.title)
        instance.thumbnail = validated_data.get("thumbnail",instance.thumbnail)
        instance.picture = validated_data.get("picture",instance.picture)
        instance.vendor = validated_data.get("vendor",instance.vendor)
        instance.description = validated_data.get("description",instance.description)
        instance.unit = validated_data.get("unit",instance.unit)
        instance.Weight = validated_data.get("Weight",instance.Weight)
        instance.desiredـtitle = validated_data.get("desiredـtitle",instance.desiredـtitle)
        instance.value = validated_data.get("value",instance.value)
        instance.current_price = validated_data.get("current_price",instance.current_price)
        instance.category =validated_data.get("category",instance.category)
        instance.save()
        return instance


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartModel
        fields= '__all__'


