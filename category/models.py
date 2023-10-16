# from djongo import models
from django.db import models
class CategoryModel(models.Model):
    title=models.CharField(max_length=255)
    parent=models.ForeignKey(to="self",on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.title

    class Meta:
        db_table="category"



# class SubCategoryModel(models.Model):
#     name = models.CharField(max_length=200)
#     category=models.ArrayReferenceField(
#         to=CategoryModel,
#         on_delete=models.CASCADE
#     )
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table="subcategory"

