# from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from category.models import SubCategoryModel
import datetime
from djongo import models
from django import forms



class ProductModel(models.Model):
    title=models.CharField(max_length=255)
    thumbnail=models.ImageField(upload_to='thumnails/',blank=True,null=True)
    picture=models.ImageField(upload_to="pictures/",blank=True,null=True)
    vendor=models.CharField(max_length=50)
    description=models.CharField(max_length=255)
    unit=models.CharField(max_length=50,default="kg")
    Weight=models.IntegerField()
    desiredـtitle=models.CharField(max_length=255,default="height")     #this can be Height or Diameter
    value=models.FloatField()     #this is the value of Height or Diameter
    current_price=models.IntegerField()
    category=models.ArrayReferenceField(to=SubCategoryModel,on_delete=models.CASCADE)
    # category=models.ForeignKey(CategoryModel,on_delete=models.CASCADE,default="",blank=True)
    class Meta:
        db_table = "products"

@receiver(post_save,sender=ProductModel)
def post_save_handler(sender,instance,**kwargs):
    obj=ChartModel(price=instance.current_price,date=datetime.datetime.now(),product_id=instance)
    obj.save()



class ChartModel(models.Model):
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    product_id=models.ForeignKey(ProductModel,on_delete=models.CASCADE)

    class Meta:
        db_table = "chart"




# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = ProductModel
#         fields = (
#             'title', 'thumbnail','picture'
#         )


# {
#     "title" : "rozhan",
#     "vendor":  "rozhan",
#     "description" : "this is  rozhan",
#     "unit" : "kg",
#     "Weight" : 20,
#     "desiredـtitle" : "height",
#     "value" : 12.5 ,
#     "current_price" : 2000,
#     "category" : 17
# }


# {
#     "title" : "bahar",
#     "thumbnail":null,
#     "picture":null,
#     "vendor":  "rozhan",
#     "description" : "this is  rozhan",
#     "unit" : "kg",
#     "Weight" : 20,
#     "desiredـtitle" : "height",
#     "value" : 12.5 ,
#     "current_price" : 2000,
#     "category" : 17
# }