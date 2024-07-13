from django.urls import path
from . import views

urlpatterns = [
  path('featured-products/', views.FeaturedProductView.as_view()),
  path('products/', views.ProductView.as_view()),
  path('products/<int:pk>/', views.SingleProductView.as_view()),
  path('product-items/', views.ProductItemView.as_view()),
  path('product-items/<int:pk>/', views.SingleProductItemView.as_view()),
  path('products/<int:pk>/product-items/', views.ProductItemsOfProduct.as_view()),
  path('filtered-product-items/', views.ProductItemsByVariationView.as_view()),
]
