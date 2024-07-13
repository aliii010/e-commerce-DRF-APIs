from rest_framework import serializers
from .models import Product, ProductItem, Variation, VariationOption
from categories.serializers import ProductCategorySerializer


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ['id', 'value']


class VariationSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    options = serializers.SerializerMethodField()
    class Meta:
        model = Variation
        fields = ['id', 'name', 'category', 'options']
        
    def get_options(self, obj):
        options = VariationOption.objects.filter(variation=obj)
        return OptionSerializer(options, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    variations = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'image', 'base_price', 'variations']
        
    def get_variations(self, obj):
        variations = Variation.objects.filter(category=obj.category)
        return VariationSerializer(variations, many=True).data


class VariationOptionSerializer(serializers.ModelSerializer):
    variation = VariationSerializer()
    class Meta:
        model = VariationOption
        fields = ['id', 'value', 'variation']



class ProductItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    variation_options = VariationOptionSerializer(many=True)

    class Meta:
        model = ProductItem
        fields = ['id', 'qty_in_stock', 'price', 'image', 'variation_options']



class ProductItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = "__all__"