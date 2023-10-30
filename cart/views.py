from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from cart.models import Order,OrderItems
from rest_framework.exceptions import AuthenticationFailed
from home.utils.token import Token
from cart.serializers import OrderSerializer,OrderItemsSerializer,CartSerializer
from users.models import User
from home.middleware.authMiddleware import JwtMiddleware
# from django.utils.decorators import method_decorator
# from home.middleware.authMiddleware //import CheckJwtMiddleware,custom_middleware_decorator


# @method_decorator(CheckJwtMiddleware,name='dispatch')
class AddToCart(APIView):
    # @AdminAuthMiddleware
    def post(self,request:Request):
        print(request.decoded)
        # token = request.META.get('HTTP_AUTHORIZATION', '')
        # if not token:
        #     raise AuthenticationFailed
        # decoded_token = Token.decodeToken(token)
        order = Order.objects.filter(user=request.decoded["id"]).first()
        try:
            if not order:
                user = User.objects.filter(id=request.decoded["id"]).first()
                newOrder=Order.objects.create(user=user)
                request.data['user'] = request.decoded["id"]
                print(request.data)

                orderItemSerializer = OrderItemsSerializer(data=request.data)

                if orderItemSerializer.is_valid(raise_exception=True):
                    orderItemSerializer.save()
                    newOrder.orderItems.add(orderItemSerializer.data["id"])

                    return Response({"data": "Item added to your cart."}, status.HTTP_200_OK)

            else:
                request.data['user'] = request.decoded["id"]
                orderItem=OrderItems.objects.filter(user=request.decoded["id"],product=request.data['product']).first()

                if not orderItem:
                    orderItemSerializer = OrderItemsSerializer(data=request.data)
                    if orderItemSerializer.is_valid(raise_exception=True):
                        orderItemSerializer.save()
                        # print(orderItemSerializer.data)
                        order.orderItems.add(orderItemSerializer.data['id'])

                        return Response({"data": "Item added to your cart."}, status.HTTP_200_OK)

                return Response({"data": "this product exists in your cart.to change your cart go to your bascket cart"}, status.HTTP_200_OK)

        except Exception as e:
            return Response({"data": str(e)}, status.HTTP_400_BAD_REQUEST)





class CartList(APIView):
   
    def get(self,request:Request):
        order=Order.objects.filter(user=request.decoded['id']).first()
        serializer=CartSerializer(order)
        return Response(serializer.data,status.HTTP_200_OK)
    
    
        
class CartDetail(APIView):
    def get_order(self,user_id,pk:int):
        orderItem=OrderItems.objects.filter(user=user_id,id=pk).first()
        return orderItem
    
    def delete(self,request:Request,pk):
        user_id=request.decoded['id']
        orderItem=self.get_order(user_id,pk)
        orderItem.delete()
        return Response({"message":"item deleted from your cart"},status.HTTP_200_OK)
        
    def put(self,request:Request,pk):
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            raise AuthenticationFailed
        orderItem=OrderItems.objects.filter(user=request.decoded['id'],id=pk).first()
        request.data['user']=request.decoded['id']
        serializer=OrderItemsSerializer(orderItem,data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)

            