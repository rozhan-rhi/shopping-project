from django.db import models
class CategoryModel(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=255,unique=True)
    parent=models.ForeignKey(to="self",related_name='category',blank=True,null=True,on_delete=models.CASCADE)

    class Meta:
        db_table="category"
