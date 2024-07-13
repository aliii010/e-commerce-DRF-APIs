from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartItemCreateSerializer


class CartListView(generics.ListAPIView):
  queryset = Cart.objects.all()
  serializer_class = CartSerializer
  permission_classes = [permissions.IsAdminUser,]



class SingleCartView(generics.RetrieveAPIView):
  queryset = Cart.objects.all()
  serializer_class = CartSerializer
  permission_classes = [permissions.IsAdminUser,]


class CartItemListView(generics.ListAPIView):
  queryset = CartItem.objects.all()
  serializer_class = CartItemSerializer
  permission_classes = [permissions.IsAdminUser]



class SingleCartItemView(generics.RetrieveAPIView):
  queryset = CartItem.objects.all()
  serializer_class = CartItemSerializer
  permission_classes = [permissions.IsAdminUser]



class CustomerSingleCartView(SingleCartView):
  permission_classes = [permissions.IsAuthenticated]
  def get_object(self):
    return get_object_or_404(Cart, customer=self.request.user)



class CustomerCartItemView(generics.ListCreateAPIView):
  serializer_class = CartItemSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user_cart = Cart.objects.get(customer=self.request.user)
    return CartItem.objects.filter(cart=user_cart)

  def post(self, request):
    cart, is_created = Cart.objects.get_or_create(customer=request.user)
    request.data['cart'] = cart.id
    serializer = CartItemCreateSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    product_item = serializer.validated_data['product_item']
    qty = serializer.validated_data['qty']

    # if this returns a cart item, it means the product already exists in the cart and it's a truthy value.
    existing_cart_item = CartItem.objects.filter(cart=cart, product_item=product_item).first()
    if existing_cart_item:
      existing_cart_item.qty += qty

      if existing_cart_item.qty > product_item.qty_in_stock:
          return Response(
              {"message": "You can't add up this product, because not enough quantity available."},
              status=status.HTTP_400_BAD_REQUEST
          )

      existing_cart_item.save()
      serializer = CartItemCreateSerializer(existing_cart_item)
      return Response(
        serializer.data, 
        status=status.HTTP_200_OK
      )

    if product_item.out_of_stock and product_item.qty_in_stock <= 0:
      return Response(
        {"message": "Product is out of stock."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if qty > product_item.qty_in_stock:
      return Response(
        {"message": "Not enough quantity available."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)



class CustomerSingleCartItemView(generics.RetrieveUpdateDestroyAPIView):
  queryset = CartItem.objects.all()
  serializer_class = CartItemSerializer
  permission_classes = [permissions.IsAuthenticated]


  # ensuring that we retrieve the cart item of that cart that belongs to the user, so that the user cannot retrieve cart items of other user's carts
  def get_object(self):
    cart_item = super().get_object()
    cart = get_object_or_404(Cart, customer=self.request.user)
    if cart_item.cart != cart:
      raise PermissionDenied({"message": "You do not have permission to access this cart item."})
    return cart_item
  
  def patch(self, request, pk):
    cart_item = self.get_object()
    entered_qty = request.data.get('qty')
    if entered_qty > cart_item.product_item.qty_in_stock:
      return Response({"message": "Not enough quantity available."})
    
    serializer = CartItemCreateSerializer(cart_item, data={'qty': entered_qty}, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

  def delete(self, request, pk):
    cart_item = self.get_object()
    cart = cart_item.cart
    self.perform_destroy(cart_item)

    remaining_cart_items = CartItem.objects.filter(cart=cart)
    serializer = CartItemSerializer(remaining_cart_items, many=True, context={'request': request})
    
    return Response(serializer.data, status=status.HTTP_200_OK)