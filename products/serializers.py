from rest_framework import serializers
from .models import ProductModel,ChartModel

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
        print(validated_data["category"])
        if product:
            raise serializers.ValidationError("there is a same product with this category!")
        return ProductModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartModel
        fields= '__all__'


