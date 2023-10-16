from rest_framework import serializers
from cart.models import Order,OrderItems

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("user","created","updated","status","orderItems","total_price")