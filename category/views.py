from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import CategoryModel
from .serializers import CategorySerializer
from django.http import Http404

class CategoryDetail(APIView):
    def get_category(self,pk):
        try:
            category = CategoryModel.objects.filter(id=pk).first()
            return category
        except CategoryModel.DoesNotExist:
            raise Http404

    def put(self, request: Request,pk):
        category=self.get_category(pk)
        serializer = CategorySerializer(category,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({"message":"error"},status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request: Request,pk):
        category=self.get_category(pk)
        category.delete()
        return Response({"message":"category deleted"}, status.HTTP_200_OK)

    def get(self, request: Request,pk):
        category=self.get_category(pk)
        serializer=CategorySerializer(category)
        return Response(serializer.data, status.HTTP_200_OK)


class CategoryList(APIView):

    def get(self,request:Request):
        categories=CategoryModel.objects.all()
        serializer=CategorySerializer(categories,many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self,request):
        print(request.POST)
        serializer=CategorySerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer.data)
            return Response(serializer.data,status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":str(e)},status.HTTP_406_NOT_ACCEPTABLE)




# class SubCategoryDetail(APIView):
#     def get_subcategory(self,pk):
#         try:
#             category = SubCategoryModel.objects.filter(id=pk).first()
#             return category
#         except SubCategoryModel.DoesNotExist:
#             raise Http404
#
#     def put(self, request: Request,pk):
#         category=self.get_subcategory(pk)
#         serializer = SubCategorySerializer(category,data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status.HTTP_200_OK)
#         return Response({"message":"error"},status.HTTP_406_NOT_ACCEPTABLE)
#
#     def delete(self, request: Request,pk):
#         category=self.get_subcategory(pk)
#         category.delete()
#         return Response({"message":"category deleted"}, status.HTTP_200_OK)
#
#     def get(self, request: Request,pk):
#         category=self.get_subcategory(pk)
#         serializer=SubCategorySerializer(category)
#         return Response(serializer.data, status.HTTP_200_OK)
#
#
# class SubCategoryList(APIView):
#     def get(self,request:Request):
#         parent=self.request.query_params.get("category")
#         categories=SubCategoryModel.objects.all()
#         if parent:
#             category=CategoryModel.objects.filter(title=parent).first()
#             categories = SubCategoryModel.objects.filter(category=category.id)
#             print(category,categories)
#         serializer=SubCategorySerializer(categories,many=True)
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     def post(self,request):
#         print(request.data)
#         serializer=SubCategorySerializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data,status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"message":str(e)},status.HTTP_406_NOT_ACCEPTABLE)



