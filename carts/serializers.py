from rest_framework import serializers
from .models import Cart, CartItem
from users.serializers import UserCreateSerializer
from products.serializers.product_item_serializers import ProductItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
  cart = serializers.HyperlinkedRelatedField(view_name='single-cart', read_only=True)
  product_item = ProductItemSerializer()
  price = serializers.SerializerMethodField(method_name='get_price')
  class Meta:
    model = CartItem
    fields = ('id', 'cart', 'product_item', 'qty', 'price')

  def get_price(self, obj):
    return obj.get_price()


class CartItemCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = CartItem
    fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
  customer = UserCreateSerializer()
  # cart_items = CartItemSerializer(many=True, read_only=True)
  cart_items = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='single-cart-item')
  total_price = serializers.SerializerMethodField(method_name='get_total_price')
  class Meta:
    model = Cart
    fields = ('id', 'customer', 'cart_items', 'total_price')

  def get_total_price(self, obj):
    return obj.get_total_price()


class CartCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cart
    fields = "__all__"