from rest_framework import serializers
from cart.models import Order,OrderItems

class OrderSerializer(serializers.ModelSerializer):
    # total_price=serializers.Field()
    class Meta:
        model=Order
        fields='__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    price=serializers.ReadOnlyField()
    class Meta:
        model = OrderItems
        fields = ['id','user','product','length','width','Height','quentity','price']


class CartSerializer(serializers.ModelSerializer):
    orderItems=OrderItemsSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ("user","created","updated","status","orderItems","total_price")