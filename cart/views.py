from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from cart.models import Order,OrderItems
from rest_framework.exceptions import AuthenticationFailed
from home.utils.token import Token
from cart.serializers import OrderSerializer,OrderItemsSerializer,CartSerializer
from users.models import User


class AddToCart(APIView):
    def post(self,request:Request):
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            raise AuthenticationFailed
        decoded_token = Token.decodeToken(token)
        order = Order.objects.filter(user=decoded_token["id"]).first()
        try:
            if not order:
                user = User.objects.filter(id=decoded_token["id"]).first()
                Order.objects.create(user=user)
                request.data['user'] = decoded_token["id"]
                print(request.data)

                orderItemSerializer = OrderItemsSerializer(data=request.data)

                if orderItemSerializer.is_valid(raise_exception=True):
                    orderItemSerializer.save()
                    return Response({"data": "Item added to your cart."}, status.HTTP_200_OK)

            else:
                request.data['user'] = decoded_token["id"]
                print(request.data)
                orderItem=OrderItems.objects.filter(user=decoded_token["id"],product=request.data['product']).first()
                print(orderItem)

                if not orderItem:
                    orderItemSerializer = OrderItemsSerializer(data=request.data)
                    if orderItemSerializer.is_valid(raise_exception=True):
                        orderItemSerializer.save()
                        return Response({"data": "Item added to your cart."}, status.HTTP_200_OK)

                return Response({"data": "this product exists in your cart.to change your cart go to your bascket cart"}, status.HTTP_200_OK)

        except Exception as e:
            return Response({"data": str(e)}, status.HTTP_400_BAD_REQUEST)



# class DeleteFromCart(APIView):
#     def get_product(self,pk):
#         orderItem=OrderItems.objects.filter(id=pk).first()
#         return orderItem
#     def delete(self,pk):


class ShowCart(APIView):
    def get(self,request:Request):
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            raise AuthenticationFailed
        decoded_token = Token.decodeToken(token)
        order=Order.objects.filter(user=decoded_token['id']).first()
        # orderItems=OrderItems.objects.filter(order=orderId)
        print(order)
        # order['orderItems']=OrderItems.objects.filter(user=decoded_token['id'])
        serializer=CartSerializer(order)
        for item in OrderItems.objects.filter(user=decoded_token['id']):
            print(item)
            # if not order.objects.filter(order=order,orderitems=item):
            order.orderItems.add(item )
        order.save()
        return Response(serializer.data,status.HTTP_200_OK)