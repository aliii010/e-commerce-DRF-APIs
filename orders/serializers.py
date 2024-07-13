from rest_framework import serializers
from users.serializers import UserCreateSerializer
from .models import Order, OrderItem
from products.serializers.product_item_serializers import ProductItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.HyperlinkedRelatedField(view_name='single-order', read_only=True)
    product_item = ProductItemSerializer()
    price = serializers.SerializerMethodField(method_name='get_price')

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product_item', 'qty', 'price')

    def get_price(self, obj):
        return obj.get_price()


class OrderSerializer(serializers.ModelSerializer):
    customer = UserCreateSerializer()
    # order_items = OrderItemSerializer(many=True, read_only=True)
    order_items = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='single-order-item')
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Order
        fields = ('id', 'customer', 'order_items', 'total_price', 'date', 'shipping_address', 'status')

    def get_total_price(self, obj: Order):
        return obj.get_total_price()
