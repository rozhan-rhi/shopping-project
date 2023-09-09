from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import ProductModel
from products.serializers import ProductListSerializer,ProductDetailSerializer
from drf_yasg.utils import swagger_auto_schema
from home.utils import token
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from django.http import Http404


class ProductDetail(APIView):
    def get_product(self, pk: int):
        try:
            product = ProductModel.objects.get(id=pk)
            return product
        except ProductModel.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk):
        product = self.get_product(pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pk):
        product = self.get_product(pk)
        product.delete()
        return Response({"message":"product deleted!"}, status.HTTP_200_OK)

    def put(self, request: Request, pk):
        product = self.get_product(pk)
        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({"message": "error"}, status.HTTP_406_NOT_ACCEPTABLE)


class ProductsListCreate(APIView):

    def post(self, request: Request):
        product = request.data
        # print(product)
        serializer = ProductDetailSerializer(data=product)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                # print(serializer.data)
                return Response({"message": "new product saved!"}, status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({"message": "try another title name,this title exists!"}, status.HTTP_400_BAD_REQUEST)

    def get(self,request:Request):
        allProducts = ProductModel.objects.all()
        serializer = ProductListSerializer(allProducts, many=True)
        return Response({"message": serializer.data}, status.HTTP_200_OK)
