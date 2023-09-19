from rest_framework import serializers
from .models import CategoryModel
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=CategoryModel
        fields='__all__'

    def create(self,validate_data):
        parent=CategoryModel.objects.filter(validate_data['parent_id']).first()
        category_item=CategoryModel.objects.create(
            title=validate_data['title'],
            parent=parent
        )
        category_item.save()
        return category_item