from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime

class ProductModel(models.Model):

    title=models.CharField(max_length=255,unique=True)
    # thumbnail=models.ImageField(upload_to='photos')
    # picture=models.ImageField(upload_to='photos')
    vendor=models.CharField(max_length=50)
    description=models.CharField(max_length=255)
    unit=models.CharField(max_length=50,default="kg")
    Weight=models.IntegerField()
    desiredـtitle=models.CharField(max_length=255,default="height")     #this can be Height or Diameter
    value=models.FloatField()     #this is the value of Height or Diameter
    current_price=models.IntegerField()
    class Meta:
        db_table = "products"

@receiver(post_save,sender=ProductModel)
def post_save_handler(sender,instance,**kwargs):
    obj=ChartModel(price=instance.current_price,date=datetime.datetime.now(),product_id=instance)
    obj.save()



class ChartModel(models.Model):
    price=models.IntegerField()
    date=models.DateField()
    product_id=models.ForeignKey(ProductModel,on_delete=models.CASCADE)

    class Meta:
        db_table = "chart"


class Category(models.Model):
    title=models.CharField(max_length=255)
    parent=models.ForeignKey(to="self",blank=True,null=True,on_delete=models.CASCADE)