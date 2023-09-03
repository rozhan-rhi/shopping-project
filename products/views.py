from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import ProductModel
from products.serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema



class ProductDetail(APIView):

    def post(self,request:Request):
        product=Request.data
        serializer=ProductSerializer(data=Request.DATA,files=Request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":serializer.data},status.HTTP_201_CREATED)

    def get(self,request:Request):
        prod_id=request.get("pk")
        product=ProductModel.objects.filter(pk=prod_id).first()
        print(product)
        serializer=ProductSerializer(product)


class ProductsList(APIView):

    def get(self):
        allProducts=ProductModel.objects.all()
        serializer=ProductSerializer(allProducts,many=True)
        return Response({"message":serializer.data},status.HTTP_200_OK)