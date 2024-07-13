from rest_framework import serializers
from ..models import Product, ProductItem, Variation, VariationOption
from categories.serializers import ProductCategorySerializer


class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = "__all__"
    
    
class VariationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Variation
    fields = "__all__"


class VariationOptionSerializer(serializers.ModelSerializer):
    variation = VariationSerializer()
    class Meta:
        model = VariationOption
        fields = ['id', 'value', 'variation']


class ProductItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    variation_options = VariationOptionSerializer(many=True)

    class Meta:
        model = ProductItem
        fields = ['id', 'product', 'qty_in_stock', 'price', 'image', 'variation_options']



class ProductItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = "__all__"