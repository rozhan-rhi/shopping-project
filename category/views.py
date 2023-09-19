from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import CategoryModel
from .serializers import CategorySerializer
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema


class CategoryDetail(APIView):
    def get_category(self,pk):
        try:
            category = CategoryModel.objects.filter(id=pk).first()
            return category
        except CategoryModel.DoesNotExist:
            raise Http404

    def post(self,request:Request):
        # parent=request.data["parent"]
        # parent_id=CategoryModel.objects.filter(title=parent)
        serializer=CategorySerializer(data=request.data)        #context={'parent':request.data["parent"]}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({"message":"error"})

    def put(self, request: Request,pk):
        category=self.get_category(pk)
        parent = request.parent
        serializer = CategorySerializer(data=request.data, context={'parent': parent})

    def delete(self, request: Request,pk):
        category=self.get_category(pk)
        category.delete()
