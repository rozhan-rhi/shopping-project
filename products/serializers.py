from rest_framework import serializers
from .models import ProductModel,ChartModel

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields=('id','title','description','current_price','thumbnail')




class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields='__all__'
            # ('id','title','vendor','description','unit','Weight','desiredـtitle','value','current_price','thumbnail','picture')
        # extra_kwargs = {
        #     "thumbnail": {"write_only": True}
        # }

    # def validate(self, kwargs):
    #     existance=ProductModel.objects.filter(title=kwargs["title"]).first()
    #     if existance:
    #         raise serializers.ValidationError("product with this name exists!")


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartModel
        fields= '__all__'


