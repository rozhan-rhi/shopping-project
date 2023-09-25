from rest_framework import serializers
from .models import ProductModel,ChartModel
from category.serializers import CategorySerializer

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields=('id','title','description','current_price','thumbnail')

    def validate(self, attrs):
        product=ProductModel.objects.filter(title=attrs["title"],category=attrs["category"]).first()
        print(attrs["category"])
        if product:
            raise serializers.ValidationError("there is a same product with this category!")




class ProductDetailSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model = ProductModel
        fields='__all__'
            # ('id','title','vendor','description','unit','Weight','desiredـtitle','value','current_price','thumbnail','picture')
        extra_kwargs = {
            "thumbnail": {"write_only": True}
        }


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartModel
        fields= '__all__'


