from rest_framework import serializers
from ..models import Product, ProductItem, Variation, VariationOption
from categories.serializers import ProductCategorySerializer
from .product_item_serializers import ProductItemSerializer

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
    default_product_item = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'image', 'base_price', 'variations', 'default_product_item']

    def get_variations(self, obj):
        variations = Variation.objects.filter(category=obj.category)
        return VariationSerializer(variations, many=True).data

    def get_default_product_item(self, obj):
        try:
            # Adjusting the image path to match the expected path for product item images
            # Product images and product item images are stored in different directories.
            # Here, we transform the product image path to match the product item image path
            # in order to retrieve the product item with the same image as the product.
            product_image = "product-item-images/" + str(obj.image).split('/')[-1]
            product_item = ProductItem.objects.get(product=obj, image=product_image)
            
            # To serialize the ProductItem with the correct absolute image path, 
            # we pass the request context from the current serializer to ProductItemSerializer.
            request = self.context.get('request')
            return ProductItemSerializer(product_item, context={'request': request}).data
        except ProductItem.DoesNotExist:
            return None
