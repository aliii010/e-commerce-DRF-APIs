from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.db import transaction
from .models import Order, OrderStatus, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from carts.models import Cart, CartItem


class OrderView(generics.ListCreateAPIView):
  serializer_class = OrderSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    if not self.request.user.is_staff:
      return Order.objects.filter(customer=self.request.user)
    return Order.objects.all()
  

  def post(self, request):
    cart = Cart.objects.get(customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
      return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

    try:
      # using transaction to ensure the atomicity, if any of the operations fail then the entire thing will roll back as nothing happened.
      with transaction.atomic():
        # create an order for the user
        order = Order.objects.create(
          customer=request.user,
          date=timezone.now().today(),
          shipping_address=request.data.get('shipping_address'),
          status=OrderStatus.objects.get(status='Confirmed')
        )

        # create order items from the user's cart items
        for item in cart_items:
          OrderItem.objects.create(
            order=order, 
            product_item=item.product_item, 
            qty=item.qty
          )
          # update quantity of the ordered product items
          item.product_item.qty_in_stock -= item.qty
          item.product_item.save()

        cart_items.delete()
      return Response({"message": "Order has been placed successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({"error": "Failed to place the order. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SingleOrderView(generics.RetrieveAPIView):
  queryset = Order.objects.all()
  serializer_class = OrderSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    order = super().get_object()
    if not self.request.user.is_staff:
      if order.customer != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to access this order."})
    return order
  


class OrderItemView(generics.ListAPIView):
  serializer_class = OrderItemSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    if not self.request.user.is_staff:
      return OrderItem.objects.filter(order__customer=self.request.user)
    return OrderItem.objects.all()
  

class SingleOrderItemView(generics.RetrieveAPIView):
  queryset = OrderItem.objects.all()
  serializer_class = OrderItemSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    order_item = super().get_object()
    if not self.request.user.is_staff:
      if order_item.order.customer != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to access this order item."})
    return order_item