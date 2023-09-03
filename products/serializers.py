from rest_framework import serializers
from .models import ProductModel
from .models import PriceChange
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields='__all__'


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceChange
        fields= '__all__'