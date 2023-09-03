from django.db import models
class ProductModel(models.Model):
    title=models.CharField(max_length=255)
    thumbnail=models.ImageField(upload_to='photos')
    picture=models.ImageField(upload_to='photos')
    vendor=models.CharField(max_length=50)
    description=models.CharField(max_length=255)
    unit=models.CharField(max_length=50,default="kg")
    Weight=models.IntegerField()
    desiredـtitle=models.CharField(max_length=255,default="height")
    value=models.IntegerField()
    current_price=models.IntegerField()
    # signal=object


class PriceChange(models.Model):
    price=models.IntegerField()
    date=models.DateField()
    product_id=models.ForeignKey(ProductModel,on_delete=models.CASCADE)