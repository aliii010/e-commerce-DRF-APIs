from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from .models import ProductCategory
from .serializers import ProductCategorySerializer
from products.models import Product, Variation
from products.serializers.product_serializers import ProductSerializer
from products.serializers.product_item_serializers import VariationSerializer


class PermissionMixin:
  def get_permissions(self):
    permission_classes = []
    if not self.request.method in permissions.SAFE_METHODS:
      permission_classes = [permissions.IsAdminUser]

    return [permission() for permission in permission_classes]
  

class CategoryView(PermissionMixin, generics.ListCreateAPIView):
  queryset = ProductCategory.objects.all()
  serializer_class = ProductCategorySerializer


class SingleCategoryView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
  queryset = ProductCategory.objects.all()
  serializer_class = ProductCategorySerializer


class CategoryProducts(APIView):
  def get(self, request, pk):
    products = Product.objects.filter(category__id=pk)
    serializer = ProductSerializer(products, many=True, context={'request': request})

    return Response(serializer.data)
  

class CategoryVariations(APIView):
  def get(self, request, pk):
    variations = Variation.objects.filter(category__id=pk)
    return Response(VariationSerializer(variations, many=True).data)


class Subcategories(APIView):
  def get(self, request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    subcategories = category.subcategories.all()

    serializer = ProductCategorySerializer(subcategories, many=True)
    return Response(serializer.data)