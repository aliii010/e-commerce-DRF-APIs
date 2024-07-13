from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Product, ProductItem
from .serializers.product_serializers import ProductSerializer
from .serializers.product_item_serializers import ProductItemSerializer, ProductItemCreateSerializer


class PermissionsMixin:
  def get_permissions(self):
    permission_classes = []
    if not self.request.method in permissions.SAFE_METHODS:
      permission_classes = [permissions.IsAdminUser]

    return [permission() for permission in permission_classes]
  

class FeaturedProductView(generics.ListAPIView):
  queryset = Product.objects.filter(featured=True)
  serializer_class = ProductSerializer
  

class ProductView(PermissionsMixin, generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer



class SingleProductView(PermissionsMixin, generics.RetrieveUpdateDestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  


class ProductItemView(PermissionsMixin, generics.ListCreateAPIView):
  queryset = ProductItem.objects.all()

  def get_serializer_class(self):
    if self.request.method == "POST":
      return ProductItemCreateSerializer
    return ProductItemSerializer


class SingleProductItemView(PermissionsMixin, generics.RetrieveUpdateDestroyAPIView):
  queryset = ProductItem.objects.all()

  def get_serializer_class(self):
    if self.request.method in ("PATCH", "PUT"):
      return ProductItemCreateSerializer
    return ProductItemSerializer


class ProductItemsOfProduct(APIView):
  def get(self, request, pk):
    product_items = ProductItem.objects.filter(product__id=pk)
    # the request object needs to be passed to the context of the serializer otherwise you won't get the absolute path for the image field
    serializer = ProductItemSerializer(product_items, many=True,  context={'request': request})
    print(serializer.context)
    return Response(serializer.data)
  

class ProductItemsByVariationView(APIView):
  def get(self, request):
    product_id = request.query_params.get('product')
    option_ids = request.query_params.getlist('options[]') # when an array is passed as a query parameter, the key from "options" becomes "options[]".
    
    product_items = ProductItem.objects.filter(product__id=product_id)
    
    if option_ids:
      for option_id in option_ids:
        product_items = product_items.filter(variation_options__id=option_id)
    
    serializer = ProductItemSerializer(product_items, many=True,  context={'request': request})
    return Response(serializer.data)