from django.db import models
from products.models import ProductModel
from users.models import User

class OrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name='items')
    length=models.FloatField()
    width=models.FloatField()
    Height=models.FloatField()
    quentity=models.IntegerField(default=1)
    # price=models.FloatField()

    @property
    def price(self):
        return self.length * self.width * self.Height * self.quentity

    class Meta:
        db_table="orderItems"

class Order (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    orderItems=models.ManyToManyField(OrderItems)


    def __str__(self):
        return f"{self.user}-orderid:{self.id}"

    @property
    def total_price(self):
        return sum(item.price for item in OrderItems.objects.filter(user=self.user))

    class Meta:
        db_table = "orders"