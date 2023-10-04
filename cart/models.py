from djongo import models
from products.models import ProductModel

class CartModel(models.Model):
    products=models.ArrayField(model_container=ProductModel,default=ProductModel)

    class Meta:
        db_table="cart"


    objects = models.DjongoManager()