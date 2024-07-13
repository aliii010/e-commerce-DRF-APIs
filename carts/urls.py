from django.urls import path
from . import views

urlpatterns = [
  # admin endpoints
  path('carts/', views.CartListView.as_view()),
  path('carts/<int:pk>/', views.SingleCartView.as_view(), name='single-cart'),
  path('cart-items/', views.CartItemListView.as_view()),
  path('cart-items/<int:pk>/', views.SingleCartItemView.as_view()),

  # customer endpoints
  path('cart/', views.CustomerSingleCartView.as_view()),
  path('cart/items/', views.CustomerCartItemView.as_view()),
  path('cart/items/<int:pk>/', views.CustomerSingleCartItemView.as_view(), name='single-cart-item')
]
